import { create } from "zustand";

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  setTokens: (accessToken: string, refreshToken: string) => void;
  setUser: (user: User | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => {
  const isBrowser = typeof window !== "undefined";
  const storedAccess = isBrowser ? localStorage.getItem("access_token") : null;
  const storedRefresh = isBrowser ? localStorage.getItem("refresh_token") : null;
  const storedUser = isBrowser ? localStorage.getItem("user") : null;

  return {
    user: storedUser ? JSON.parse(storedUser) : null,
    accessToken: storedAccess,
    refreshToken: storedRefresh,
    isAuthenticated: !!storedAccess,

    setTokens: (accessToken: string, refreshToken: string) => {
      if (isBrowser) {
        localStorage.setItem("access_token", accessToken);
        localStorage.setItem("refresh_token", refreshToken);
      }
      set({ accessToken, refreshToken, isAuthenticated: true });
    },

    setUser: (user: User | null) => {
      if (isBrowser) {
        if (user) {
          localStorage.setItem("user", JSON.stringify(user));
        } else {
          localStorage.removeItem("user");
        }
      }
      set({ user });
    },

    logout: () => {
      if (isBrowser) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
      }
      set({
        user: null,
        accessToken: null,
        refreshToken: null,
        isAuthenticated: false,
      });
    },
  };
});
