import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Home from "./pages/Home";
import FreeChat from "./pages/FreeChat";
import MemoryHome from "./pages/MemoryHome";
import ProtectedRoute from "./components/ProtectedRoute";

export default function App() {
  return (
    <Routes>
      {/* PUBLIC */}
      <Route path="/login" element={<Login />} />

      {/* HOME */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />

      {/* FREE CHAT */}
      <Route
        path="/free-chat"
        element={
          <ProtectedRoute>
            <FreeChat />
          </ProtectedRoute>
        }
      />

      {/* MEMORY BASED */}
      <Route
        path="/memory"
        element={
          <ProtectedRoute>
            <MemoryHome />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
