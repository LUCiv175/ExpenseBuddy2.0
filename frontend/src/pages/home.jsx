import React, { useContext, useState, useEffect } from "react";
import { GroupContext } from "../contexts/GroupContext";
import DebtCard from "../components/DebtCard";  // Import DebtCard from the components folder

const Home = () => {
  const { currentGroup } = useContext(GroupContext);
  const [groups, setGroups] = useState([]);  // Inizializza groups come array vuoto

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        const res = await fetch('http://127.0.0.1:5000/get_total_debt_by_group');
        const data = await res.json();
        console.log(data);
        setGroups(data);
      } catch (error) {
        console.error('Errore durante il fetch dei dati:', error);
      }
    };

    fetchGroups();  // Chiama la funzione fetchGroups
  }, []);

  return (
    <div className="min-h-screen m-5">
      {groups.length > 0 ? (  // Controlla se groups ha dati
        <DebtCard 
          amount={groups[0].diff}  // Usa il valore groups[0].diff solo se disponibile
        />
      ) : (
        <p>Caricamento...</p>  // Mostra un messaggio di caricamento mentre i dati non sono pronti
      )}
    </div>
  );
};

export default Home;
