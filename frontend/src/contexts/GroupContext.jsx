import React, { createContext, useState } from "react";
export const GroupContext = createContext();
const GroupContextProvider = ({ children, selectedCookieGroup }) => {
  const [currentGroup, setCurrentGroup] = useState(selectedCookieGroup);
  const [allGroups, setAllGroups] = useState([
    { id: "a", name: "group1" },
    { id: "b", name: "group2" },
    { id: "c", name: "group3" },
  ]);
  return (
    <GroupContext.Provider
      value={{
        currentGroup,
        setCurrentGroup,
        allGroups,
      }}
    >
      {children}
    </GroupContext.Provider>
  );
};
export default GroupContextProvider;
