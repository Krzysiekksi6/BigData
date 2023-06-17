import React, { useEffect, useState } from 'react';
import LoadingSpinner from '../UI/LoadingSpinner/LoadingSpinner';
import CurrencyItem from "./CurrencyItem";
import classes from './AvailableData.module.css'
const AvailableData = () => {
    const [items, setItems] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [httpError, setHttpError] = useState(null);
    const URL = 'http://127.0.0.1:5000/currency';
    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch(
                URL
            );

            if (!response.ok) {
                throw new Error(
                    'Something went wrong, you cannot connect to database...'
                );
            }
            const responseData = await response.json();
            const parseData = responseData.Rates
            const loadedData = [];
            for (const key in parseData) {
                loadedData.push({
                    currency: parseData[key].currency,
                    currencySymbol: parseData[key].code,
                    value: parseData[key].mid,
                });
            }

            setItems(loadedData);
            setIsLoading(false);
        };

        fetchData().catch((error) => {
            setIsLoading(false);
            setHttpError(error.message);
        });
    }, []);

    if (isLoading) {
        return (
            <section>
                <LoadingSpinner />
            </section>
        );
    }

    if (httpError) {
        return (
            <section>
                <h3 className={classes['http-error']}>{httpError}...</h3>
            </section>
        );
    }
    const dataList = items.map((item, index) => (
        <CurrencyItem
            key={index}
            currency={item.currency}
            currencySymbol={item.currencySymbol}
            value={item.value}
        />
    ));

    return (
        <section className={classes['data']}>
            <ul>{dataList}</ul>
        </section>
    );
};

export default AvailableData;
