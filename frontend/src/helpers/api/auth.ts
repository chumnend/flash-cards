import { client } from './client'
import type {
    ApiStatusResponse,
    AuthResponse,
    RegisterPayload,
    LoginPayload
} from '..//types/api';


export const checkApiStatus = () =>
  client.get<ApiStatusResponse>('/status')

export const registerUser = (payload: RegisterPayload) =>
  client.post<AuthResponse>('/register', payload)

export const loginUser = (payload: LoginPayload) =>
  client.post<AuthResponse>('/login', payload)