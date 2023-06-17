import React from 'react';
import Icon from '../../UI/Icons/Icon'
import styles from './Navbar.module.css';

const Navbar = () => {
    return (
        <React.Fragment>
            <nav className={styles.header}>
                <div className={styles.heading}>
                    <h2>
                        <span>exchange</span>Currency
                    </h2>
                </div>
                <div className={styles.logo}>
					<span className={styles.icon}>
						<Icon />
					</span>
                </div>
            </nav>

        </React.Fragment>
    );
};

export default Navbar;
