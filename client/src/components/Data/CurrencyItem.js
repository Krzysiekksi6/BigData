import React from 'react';
import classes from './CurrencyItem.module.css'
const CurrencyItem = ({
    id,
    currency,
    currencySymbol,
    value
}) => {
    return (
        <li key={id} className={classes['data__box']}>

            {/*<img src="img/icons/briefcase.svg" alt="" className="plans__item plans__item-icon">*/}

                <div className={classes['data__item-name']}>
                    <p><b>Currency:</b></p>
                    <h3 className={classes.value}>{currency}</h3>
                </div>
                <div className={`${classes['data__item']}`}>
                    <p><b>Symbol:</b></p>
                    <p className={classes.value}>{currencySymbol}</p>
                </div>
                <div className={classes['data__item']}>
                    <p><b>Value:</b></p>
                    <p className={classes['value-second']}>{value}</p>
                </div>

        </li>
    );
};

export default CurrencyItem;
