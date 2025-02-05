import { Routes, Route, BrowserRouter } from "react-router-dom";
import MainRouter from './routers/main/main_router';
import NotFoundPage from "./routers/not_found/not_found_router";
import {Box, ChakraProvider, extendTheme} from "@chakra-ui/react";
import WithAction from "./pages/top_bar.js";

// Add custom green color to theme
const theme = extendTheme({
  colors: {
    customGreen: {
      500: "#426c2c",
    },
  },
});

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
    <ChakraProvider theme={theme}>
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
