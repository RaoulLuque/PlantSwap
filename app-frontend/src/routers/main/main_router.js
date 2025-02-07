import React from "react";
import { Route, Routes } from "react-router-dom";
import PlantList from "./pages/plants";

const MainRouter = () => {
  return (
    <Routes>
      <Route path="/" element={<PlantList />} />
    </Routes>
  );
};

export default MainRouter;
