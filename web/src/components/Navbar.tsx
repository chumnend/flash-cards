import './Navbar.css'

type Props = {
    username: string,
    isLoggedIn: boolean,
    onLogin: () => void,
    onLogout: () => void,
}

const Navbar = (props: Props) => {
    const { username, isLoggedIn, onLogin, onLogout } = props;

    const SignedInNavbarMenu = (
        <div className="navbar-signed-in">
            <span className="navbar-welcome">Welcome, {username}!</span>
            <ul className="navbar-nav">
                <li><a href="/explore">Explore</a></li>
                <li><a href="/decks">Decks</a></li>
                <li><a href="/profile">Profile</a></li>
            </ul>
            <button className="navbar-btn navbar-btn-primary" onClick={onLogout}>Logout</button>
        </div>
    );

    const SignedOutNavbarMenu = (
        <div className="navbar-signed-out">
            <ul className="navbar-nav">
                <li><a href="/explore">Explore</a></li>
            </ul>
            <button className="navbar-btn navbar-btn-primary" onClick={onLogin}>Register</button>
            <button className="navbar-btn navbar-btn-outline" onClick={onLogin}>Login</button>
        </div>
    );

    return (
        <div className="navbar">
            <div className="navbar-container">
                <div className="navbar-brand">
                    <span>Flashly</span>
                </div>

                <div className="navbar-menu">
                    {isLoggedIn ? SignedInNavbarMenu : SignedOutNavbarMenu}
                </div>
            </div>
        </div>
    );
};

export default Navbar;
