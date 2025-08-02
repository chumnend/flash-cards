import { Link, useNavigate } from 'react-router-dom';

import './Navbar.css'

type Props = {
    username: string,
    isLoggedIn: boolean,
    onLogout: () => void,
}

const Navbar = (props: Props) => {
    const { username, isLoggedIn, onLogout } = props;
    const navigate = useNavigate();

    const handleRegisterClick = () => {
        navigate('/register');
    };

    const handleLoginClick = () => {
        navigate('/login');
    };

    const SignedInNavbarMenu = (
        <div className="navbar-signed-in">
            <span className="navbar-welcome">Welcome, {username}!</span>
            <ul className="navbar-nav">
                <li><Link to="/explore">Explore</Link></li>
                <li><Link to="/decks">Decks</Link></li>
                <li><Link to="/profile">Profile</Link></li>
            </ul>
            <button className="navbar-btn navbar-btn-primary" onClick={onLogout}>Logout</button>
        </div>
    );

    const SignedOutNavbarMenu = (
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
                    {isLoggedIn ? SignedInNavbarMenu : SignedOutNavbarMenu}
                </div>
            </div>
        </div>
    );
};

export default Navbar;
