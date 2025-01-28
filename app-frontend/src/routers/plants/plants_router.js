import React from "react";
import { Route, Routes } from "react-router-dom";
import PlantsPage from "./pages/plants_page";
import PlantList from "./pages/plants_list";

const PlantsRouter = () => {
  return (
    <Routes>
    {/* Routes are prefixed with /plants by declaration in App.js */}
      <Route path="/" element={<PlantsPage />} />
        <Route path="/alt" element={<PlantList/>} />
    </Routes>
  );
};

export default PlantsRouter;
