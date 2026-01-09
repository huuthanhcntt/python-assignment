import { apiClient } from './client';

export interface UserRegister {
  username: string;
  email: string;
  password: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface UserResponse {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  created_at: string;
}

export const authApi = {
  // Register a new user
  register: async (data: UserRegister): Promise<UserResponse> => {
    const response = await apiClient.post<UserResponse>('/auth/register', data);
    return response.data;
  },

  // Login and get JWT token
  login: async (credentials: UserLogin): Promise<Token> => {
    const response = await apiClient.post<Token>('/auth/login', credentials);
    return response.data;
  },

  // Get current user info
  getMe: async (): Promise<UserResponse> => {
    const response = await apiClient.get<UserResponse>('/auth/me');
    return response.data;
  },
};
