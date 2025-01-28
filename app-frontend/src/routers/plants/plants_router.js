import React from "react";
import { Route, Routes } from "react-router-dom"; // Import React Router components
import PlantsPage from "./pages/plants_page";
import PlantList from "./pages/plants_list"; // Import the PlantsPage component

const PlantsRouter = () => {
  return (
    <Routes>
      <Route path="/" element={<PlantsPage />} /> {/* Root route for /plants */}
        <Route path="/alt" element={<PlantList/>} />
    </Routes>
  );
};

export default PlantsRouter;
