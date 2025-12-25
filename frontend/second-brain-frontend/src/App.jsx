import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminRoute from "./components/AdminRoute";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Chatbot from "./pages/Chatbot";
import MemoryMode from "./pages/MemoryMode";
import Ingest from "./pages/Ingest";
import HybridSearch from "./pages/HybridSearch";

import AdminDashboard from "./pages/AdminDashboard";
import AdminUsers from "./pages/AdminUsers";
import AdminLogs from "./pages/AdminLogs";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>

        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        <Route path="/chatbot" element={
          <ProtectedRoute><Chatbot /></ProtectedRoute>
        }/>

        <Route path="/memory" element={
          <ProtectedRoute><MemoryMode /></ProtectedRoute>
        }/>

        <Route path="/ingest" element={
          <ProtectedRoute><Ingest /></ProtectedRoute>
        }/>

        <Route path="/hybrid" element={
          <ProtectedRoute><HybridSearch /></ProtectedRoute>
        }/>


        {/* ADMIN SECTION */}
        <Route path="/admin" element={
          <AdminRoute><AdminDashboard /></AdminRoute>
        }/>

        <Route path="/admin/users" element={
          <AdminRoute><AdminUsers /></AdminRoute>
        }/>

        <Route path="/admin/logs" element={
          <AdminRoute><AdminLogs /></AdminRoute>
        }/>

      </Routes>
    </BrowserRouter>
  );
}
