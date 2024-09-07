import React, { useState } from 'react';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  return (
    <header className="">
      <nav className="container mx-auto flex flex-row justify-around">
        <h1 className='text-red-500'>ciao</h1>
        <h1>prova</h1>
      </nav>
    </header>
  );
};

export default Navbar;
