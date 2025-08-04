import { Link, useNavigate } from 'react-router-dom';

import { type IAuthUser } from '../../helpers/types';

import './Navbar.css'


export type Props = {
    isLoggedIn: boolean;
    authUser: IAuthUser | null | undefined;
    onLogout: () => void;
}

const Navbar = (props: Props) => {
    const { isLoggedIn, authUser, onLogout } = props;
    const navigate = useNavigate();

    const handleRegisterClick = () => {
        navigate('/register');
    };

    const handleLoginClick = () => {
        navigate('/login');
    };

    const handleLogout = () => {
        onLogout();
    }

    const AuthenticatedNavbarMenu = (
        <div className="navbar-signed-in">
            <span className="navbar-welcome">Welcome, {authUser?.name || 'User'}!</span>
            <ul className="navbar-nav">
                <li><Link to="/feed">Your Feed</Link></li>
                <li><Link to="/explore">Explore</Link></li>
                <li><Link to="/decks">Decks</Link></li>
                <li><Link to="/profile">Profile</Link></li>
            </ul>
            <button className="navbar-btn navbar-btn-primary" onClick={handleLogout}>Logout</button>
        </div>
    );

    const UnauthenticatedNavbarMenu = (
        <div className="navbar-signed-out">
            <ul className="navbar-nav">
                <li><Link to="/explore">Explore</Link></li>
            </ul>
            <button className="navbar-btn navbar-btn-primary" onClick={handleRegisterClick}>Register</button>
            <button className="navbar-btn navbar-btn-outline" onClick={handleLoginClick}>Login</button>
        </div>
    );

    return (
        <div className="navbar">
            <div className="navbar-container">
                <div className="navbar-brand">
                    <Link to="/">Flashly</Link>
                </div>

                <div className="navbar-menu">
                    {isLoggedIn ? AuthenticatedNavbarMenu : UnauthenticatedNavbarMenu}
                </div>
            </div>
        </div>
    );
};

export default Navbar;
