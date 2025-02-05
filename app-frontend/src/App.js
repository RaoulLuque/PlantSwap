import { Routes, Route, BrowserRouter } from "react-router-dom";
import MainRouter from './routers/main/main_router';
import NotFoundPage from "./routers/not_found/not_found_router";
import {Box, ChakraProvider} from "@chakra-ui/react";
import WithAction from "./pages/top_bar.js";

// Layout component that includes the top bar
const Layout = ({ children }) => {
  return (
    <>
      <WithAction /> {/* Top bar */}
      <Box p={4}>{children}</Box> {/* Page content */}
    </>
  );
};

function App() {
  return (
    <ChakraProvider>
      <BrowserRouter>
        <div className="App">
          <Routes>
            {/* Wrap the PlantsRouter with the Layout component */}
            <Route
              path="/*"
              element={
                <Layout>
                  <MainRouter />
                </Layout>
              }
            />

            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </div>
      </BrowserRouter>
    </ChakraProvider>
  );
}

export default App;
