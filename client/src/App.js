import React from 'react';
import Navbar from "./components/Layout/Navbar/Navbar";
import AvailableData from "./components/Data/AvailableData";

function App() {
  return (
      <React.Fragment>
        <Navbar />
        <AvailableData/>
      </React.Fragment>
  );
}

export default App;
