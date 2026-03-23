import { type ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';

import { useAuth } from '../../providers/AuthProvider';

export type Props = {
    children: ReactNode;
};

const ProtectedRoute = ({ children }: Props) => {
    const { isAuthenticated } = useAuth();
    const location = useLocation();

    if (!isAuthenticated) {
        return <Navigate to="/login" replace state={{ from: location }} />;
    }

    return <>{children}</>;
};

export default ProtectedRoute;
