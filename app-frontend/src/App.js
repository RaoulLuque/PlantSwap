import {Routes, Route, BrowserRouter} from "react-router-dom";
import PlantsRouter from './routers/plants/plants_router';
import NotFoundPage from "./routers/not_found/not_found_router";
import {ChakraProvider} from "@chakra-ui/react";

function App() {
  return (
      <ChakraProvider>
        <BrowserRouter>
            <div className="App">
              <h1>Plant Swap App</h1>
              <Routes>
                {/* Include the PlantsRouter component for plants-related routes */}
                <Route path="/plants/*" element={<PlantsRouter />} />

                {/* Add the catch-all route for 404 Not Found */}
                <Route path="*" element={<NotFoundPage />} />
              </Routes>
            </div>
        </BrowserRouter>
    </ChakraProvider>
  );
}

export default App;
