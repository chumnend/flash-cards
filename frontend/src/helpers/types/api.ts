import type { User } from './user';

export type AuthResponse = {
    message: string
    user: User
    token: string
  }
  
  export type ApiStatusResponse = {
    message: string
    status: string
    timestamp: string
  }
  
  export type RegisterPayload = {
    firstName: string
    lastName: string
    username: string
    email: string
    password: string
  }
  
  export type LoginPayload = {
    email: string
    password: string
  }