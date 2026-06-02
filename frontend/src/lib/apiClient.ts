import { useAuthStore } from "@/stores/authStore";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface RequestOptions extends RequestInit {
  bodyData?: any;
}

export interface APIResponse<T> {
  success: boolean;
  message?: string;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: Record<string, string>;
  };
}

let isRefreshing = false;
let refreshSubscribers: ((token: string) => void)[] = [];

function subscribeTokenRefresh(cb: (token: string) => void) {
  refreshSubscribers.push(cb);
}

function onRefreshed(token: string) {
  refreshSubscribers.forEach((cb) => cb(token));
  refreshSubscribers = [];
}

export async function apiRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<APIResponse<T>> {
  const url = `${API_BASE_URL}${endpoint}`;

  // Build headers
  const headers = new Headers(options.headers || {});

  // Attach auth token if available
  const { accessToken, refreshToken, setTokens, logout } = useAuthStore.getState();
  if (accessToken && !headers.has("Authorization")) {
    headers.set("Authorization", `Bearer ${accessToken}`);
  }

  // Set default content type to JSON if bodyData is provided
  if (options.bodyData !== undefined && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
    options.body = JSON.stringify(options.bodyData);
  }

  const fetchOptions: RequestInit = {
    ...options,
    headers,
  };

  try {
    const response = await fetch(url, fetchOptions);

    // If unauthorized, attempt seamless token refresh
    if (
      response.status === 401 &&
      refreshToken &&
      !endpoint.includes("/auth/login") &&
      !endpoint.includes("/auth/refresh")
    ) {
      if (!isRefreshing) {
        isRefreshing = true;
        try {
          const refreshUrl = `${API_BASE_URL}/auth/refresh`;
          const refreshResponse = await fetch(refreshUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh_token: refreshToken }),
          });

          if (refreshResponse.ok) {
            const refreshResult = await refreshResponse.json();
            const { access_token, refresh_token } = refreshResult.data;

            // Update local storage and Zustand state
            setTokens(access_token, refresh_token);
            isRefreshing = false;
            onRefreshed(access_token);
          } else {
            // Token refresh expired or invalid
            isRefreshing = false;
            logout();
            if (typeof window !== "undefined") {
              window.location.href = "/login";
            }
            throw new Error("Session expired. Please log in again.");
          }
        } catch (refreshErr) {
          isRefreshing = false;
          logout();
          if (typeof window !== "undefined") {
            window.location.href = "/login";
          }
          throw refreshErr;
        }
      }

      // Queue original request until refresh completes
      return new Promise<APIResponse<T>>((resolve) => {
        subscribeTokenRefresh((newToken) => {
          headers.set("Authorization", `Bearer ${newToken}`);
          resolve(apiRequest<T>(endpoint, options));
        });
      });
    }

    const data = await response.json();
    return data as APIResponse<T>;
  } catch (error: any) {
    return {
      success: false,
      error: {
        code: "NETWORK_ERROR",
        message: error.message || "Failed to communicate with API server.",
      },
    };
  }
}
