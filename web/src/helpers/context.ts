import { useOutletContext } from 'react-router-dom';

import { type IAuthUser } from './types';

export type ContextType = {
  authUser: IAuthUser | null,
  handleRegister: (id: string, name: string, email: string, token: string) => void,
  handleLogin: (id: string, name: string, email: string, token: string) => void,
  handleLogout: () => void,
}

export const useAuthContext = () => {
  return useOutletContext<ContextType>();
}
