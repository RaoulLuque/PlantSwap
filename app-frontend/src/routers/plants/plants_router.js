import React from "react";
import { Route, Routes } from "react-router-dom"; // Import React Router components
import PlantsPage from "./pages/plants_page"; // Import the PlantsPage component

const PlantsRouter = () => {
  return (
    <Routes>
      <Route path="/" element={<PlantsPage />} /> {/* Root route for /plants */}
      {/* You can add more routes related to plants here */}
    </Routes>
  );
};

export default PlantsRouter;
