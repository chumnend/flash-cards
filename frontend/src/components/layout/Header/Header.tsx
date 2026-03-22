import { Link, useNavigate } from 'react-router-dom';

import { useAuth } from '../../providers/AuthProvider';

import './Header.css';

const Header = () => {
    const auth = useAuth();
    const navigate = useNavigate();

    const handleRegisterClick = () => {
        navigate('/register');
    };

    const handleLoginClick = () => {
        navigate('/login');
    };

    const handleLogout = () => {
        auth.logout();
        navigate('/');
    };

    const AuthenticatedMenu = (
          <div className="header-signed-in">
            <span className="header-welcome">Welcome, {auth.user?.username || 'User'}!</span>
            <ul className="header-nav">
                <li><Link to="/feed">Your Feed</Link></li>
                <li><Link to="/explore">Explore</Link></li>
                <li><Link to="/decks">Decks</Link></li>
                <li><Link to={`/settings`}>Settings</Link></li>
            </ul>
            <button className="header-btn header-btn-primary" onClick={handleLogout}>Logout</button>
        </div>      
    );

    const UnauthentictedMenu = (
        <div className="header-signed-out">
            <ul className="header-nav">
                <li><Link to="/explore">Explore</Link></li>
            </ul>
            <button className="header-btn header-btn-primary" onClick={handleRegisterClick}>Register</button>
            <button className="header-btn header-btn-outline" onClick={handleLoginClick}>Login</button>
        </div>
    );

    return (
        <div className='header'>
            <div className='header-container'>
                <div className='header-brand'>
                    <Link to="/">Flashly</Link>
                </div>
                <div className='header-menu'>
                    {auth.isAuthenticated ? AuthenticatedMenu : UnauthentictedMenu}
                </div>
            </div>
        </div>
    );
}

export default Header;
