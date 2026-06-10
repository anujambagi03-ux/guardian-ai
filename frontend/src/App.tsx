import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "./layout/MainLayout";

import Dashboard from "./pages/Dashboard";
import VehicleDetection from "./pages/VehicleDetection";
import Violations from "./pages/Violations";
import AccidentDetection from "./pages/AccidentDetection";
import Analytics from "./pages/Analytics";
import Reports from "./pages/Reports";
import Settings from "./pages/Settings";
import Monitoring from "./pages/Monitoring";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<MainLayout />}>

          <Route index element={<Dashboard />} />

          <Route
            path="monitoring"
            element={<Monitoring />}
          />

          <Route
            path="vehicles"
            element={<VehicleDetection />}
          />

          <Route
            path="violations"
            element={<Violations />}
          />

          <Route
            path="accidents"
            element={<AccidentDetection />}
          />

          <Route
            path="analytics"
            element={<Analytics />}
          />

          <Route
            path="reports"
            element={<Reports />}
          />

          <Route
            path="settings"
            element={<Settings />}
          />

        </Route>

      </Routes>
    </BrowserRouter>
  );
}

export default App;