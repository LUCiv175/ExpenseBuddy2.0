import React, { useState, useContext } from "react";
import { GroupContext } from "../contexts/GroupContext";

const Navbar = ({ onGroupChange }) => {
  const { currentGroup, setCurrentGroup, allGroups } = useContext(GroupContext);
  // Esegui il codice solo una volta all'avvio

  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleSelectGroup = (groupIndex) => {
    setCurrentGroup(groupIndex);
    setIsOpen(false); // Chiudi il dropdown una volta selezionato
    onGroupChange(groupIndex); // Aggiorna il cookie con il gruppo selezionato
  };

  return (
    <header className="bg-gray-800 text-white p-4">
      <nav className="container mx-auto flex flex-row justify-around">
        {/* Dropdown per selezionare i gruppi */}
        <div className="relative">
          <button
            onClick={toggleDropdown}
            className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded"
          >
            {
              allGroups.length > 0 && currentGroup !== null && allGroups[currentGroup]
                ? allGroups[currentGroup].name // Mostra il nome del gruppo selezionato
                : "Select a group" // Mostra "Select a group" se nessun gruppo è selezionato
            }{" "}
            {/* Nome del gruppo selezionato */}
          </button>

          {isOpen && (
            <div className="absolute mt-2 w-48 bg-white text-black rounded shadow-lg z-10">
              {allGroups.map((group, index) => (
                <a
                  key={index}
                  href="#"
                  className="block px-4 py-2 hover:bg-gray-200"
                  onClick={() => handleSelectGroup(index)} // Seleziona il gruppo
                >
                  {group.name}
                </a>
              ))}
            </div>
          )}
        </div>
      </nav>
    </header>
  );
};

export default Navbar;
