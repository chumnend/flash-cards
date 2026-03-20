import { Link } from 'react-router-dom';

import './Header.css';

const Header = () => {
    return (
        <div className='header'>
            <div className='header-container'>
                <div className='header-brand'>
                    <Link to="/">Flashly</Link>
                </div>
                <div className='header-menu'>

                </div>
            </div>
        </div>
    );
}

export default Header;
