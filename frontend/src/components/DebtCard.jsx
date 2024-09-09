import React from 'react';
import PropTypes from 'prop-types'; // Per la validazione delle props

const DebtCard = ({ creditor, amount, dueDate, description }) => {
    // Funzione per formattare l'importo
    const formatCurrency = (value) => {
        return new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR' }).format(value);
    };


    return (
        <div className="bg-white shadow-md rounded-lg py-1 px-5">
            <div className=" border-gray-200 py-2 my-2">
                <p className="text-black-600 text-xs">
                    Bilancio: 
                </p>
                <p className={`text-xl ${amount < 0 ? 'text-red-400' : 'text-green-500'}`}>
                <strong className="font-bold">{formatCurrency(amount)}</strong></p>
            </div>
        </div>
    );
};

// PropTypes per la validazione delle props
DebtCard.propTypes = {
    amount: PropTypes.number.isRequired
};

export default DebtCard;
