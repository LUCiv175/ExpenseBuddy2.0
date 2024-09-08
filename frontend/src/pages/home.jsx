import React from "react";
import { useContext } from "react";
import { GroupContext } from "../contexts/GroupContext";

const Home = () => {
  const { currentGroup, setCurrentGroup } = useContext(GroupContext);
  

  return (
    <div>
      <p>{currentGroup}</p>
    </div>
  );
};

export default Home;
