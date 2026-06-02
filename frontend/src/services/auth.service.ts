import { apiRequest, APIResponse } from "@/lib/apiClient";
import { User } from "@/stores/authStore";

export interface RegisterPayload {
  email: string;
  password?: string;
  full_name: string;
}

export interface LoginPayload {
  email: string;
  password?: string;
}

export interface TokenResponseData {
  access_token: string;
  refresh_token: string;
  expires_in: number;
}

export interface RegisterResponseData {
  user_id: string;
}

export const authService = {
  /**
   * Registers a new user.
   */
  register: async (payload: RegisterPayload): Promise<APIResponse<RegisterResponseData>> => {
    return apiRequest<RegisterResponseData>("/auth/register", {
      method: "POST",
      bodyData: payload,
    });
  },

  /**
   * Authenticates user credentials.
   */
  login: async (payload: LoginPayload): Promise<APIResponse<TokenResponseData>> => {
    return apiRequest<TokenResponseData>("/auth/login", {
      method: "POST",
      bodyData: payload,
    });
  },

  /**
   * Fetches current authenticated user profile.
   */
  getMe: async (): Promise<APIResponse<User>> => {
    return apiRequest<User>("/auth/me", {
      method: "GET",
    });
  },

  /**
   * Triggers manual token refresh.
   */
  refresh: async (refreshToken: string): Promise<APIResponse<TokenResponseData>> => {
    return apiRequest<TokenResponseData>("/auth/refresh", {
      method: "POST",
      bodyData: { refresh_token: refreshToken },
    });
  },
};
