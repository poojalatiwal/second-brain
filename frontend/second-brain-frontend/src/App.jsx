import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
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

import AdminRoute from "./components/AdminRoute";
import AdminLayout from "./pages/admin/AdminLayout"; 
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminUsers from "./pages/admin/AdminUsers";
import AdminLogs from "./pages/admin/AdminLogs";
import AdminStats from "./pages/admin/AdminStats";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/oauth-success" element={<OAuthSuccess />} />

      <Route path="/" element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />

      <Route
        path="/free-chat"
        element={
          <ProtectedRoute>
            <FreeChat />
          </ProtectedRoute>
        }
      />


      <Route
        path="/memory"
        element={
          <ProtectedRoute>
            <MemoryHome />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="text" replace />} />
        <Route path="text" element={<MemoryText />} />
        <Route path="pdf" element={<MemoryPdf />} />
        <Route path="image" element={<MemoryImage />} />
        <Route path="url" element={<MemoryUrl />} />
        <Route path="audio" element={<MemoryAudio />} />
      </Route>

      <Route path="/admin" element={<AdminRoute />}>
        <Route element={<AdminLayout />}>
          <Route index element={<AdminDashboard />} />
          <Route path="users" element={<AdminUsers />} />
          <Route path="logs" element={<AdminLogs />} />
          <Route path="stats" element={<AdminStats />} />
        </Route>
      </Route>

      <Route path="/memory-home" element={<Navigate to="/memory" replace />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
