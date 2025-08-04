import { useEffect, type ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';

import { useAuthContext } from '../../helpers/context';

export type Props = {
    children: ReactNode,
}

const ProtectedRoute = ({ children }: Props) => {
    const { authUser } = useAuthContext();
    const navigate = useNavigate();

    useEffect(() => {
        if (!authUser) {
            navigate('/login');
        }
    }, [authUser, navigate]);

    if (!authUser) {
        return null;
    }

    return <>{children}</>;
}

export default ProtectedRoute;
