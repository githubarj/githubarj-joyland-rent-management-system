import { AxiosRequestConfig } from 'axios';
export interface invoices {
  id: number;
  houseNumber: string;
  tenant: string;
  total: string;
  issueDate: Date;
  balance: number;
  type: string;
}

// Extend AxiosRequestConfig to include a _retry property
export interface AxiosRequestConfigWithRetry extends AxiosRequestConfig {
  _retry?: boolean;
}

// API response structure
export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data: T;
}
