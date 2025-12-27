import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup"; // ✅ FIXED
import Home from "./pages/Home";
import FreeChat from "./pages/FreeChat";
import MemoryHome from "./pages/MemoryHome";

import MemoryText from "./pages/MemoryText";
import MemoryPdf from "./pages/MemoryPdf";
import MemoryImage from "./pages/MemoryImage";
import MemoryUrl from "./pages/MemoryUrl";
import MemoryAudio from "./pages/MemoryAudio";

import OAuthSuccess from "./pages/OAuthSuccess";
import ProtectedRoute from "./components/ProtectedRoute";


export default function App() {
  return (
    <Routes>
      {/* PUBLIC */}
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
  <Route path="/oauth-success" element={<OAuthSuccess />} />

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

      {/* MEMORY (LAYOUT + NESTED PAGES) */}
      <Route
        path="/memory"
        element={
          <ProtectedRoute>
            <MemoryHome />
          </ProtectedRoute>
        }
      >
        <Route path="text" element={<MemoryText />} />
        <Route path="pdf" element={<MemoryPdf />} />
        <Route path="image" element={<MemoryImage />} />
        <Route path="url" element={<MemoryUrl />} />
        <Route path="audio" element={<MemoryAudio />} />
      </Route>

      {/* SAFETY REDIRECT (old URLs) */}
      <Route path="/memory-home" element={<Navigate to="/memory" replace />} />
    </Routes>
  );
}
