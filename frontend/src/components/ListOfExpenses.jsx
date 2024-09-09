import React from 'react';

function convertSQLiteDateToEuropean(sqliteDate) {
    // Verifica che la data sia nel formato 'YYYY-MM-DD'
    if (!/^\d{4}-\d{2}-\d{2}$/.test(sqliteDate)) {
        throw new Error("Formato data non valido. Usa il formato 'YYYY-MM-DD'.");
    }

    // Dividi la data in anno, mese e giorno
    const [year, month, day] = sqliteDate.split('-');

    // Restituisci la data nel formato 'DD/MM/YYYY'
    return `${day}/${month}/${year}`;
}

const ListOfExpenses = ({ expenses }) => {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4 text-center">Expenses List</h1>
      <div className="bg-white shadow-lg rounded-lg p-6">
        <ul className="divide-y divide-gray-200">
          {expenses.map((expense) => (
            <li key={expense[0]} className="py-4 flex justify-between items-center">
              <div>
                <p className="text-lg font-semibold">{expense[1]}</p>
                <p className="text-sm text-gray-500">{convertSQLiteDateToEuropean(expense[3])}</p>
                <p className="text-sm text-gray-400">User: {expense[4]}</p> {/* Muestra el nombre del usuario */}
              </div>
            <div>
            <p className="text-lg font-bold text-gray-700">€{expense[5]?.toFixed(2) || '0.00'}</p> {/* Importo */}
                {expense[5] !== expense[2] && expense[2] != null && (
                  <p className="text-sm text-gray-400">di €{expense[2]?.toFixed(2)}</p>
                )}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ListOfExpenses;
