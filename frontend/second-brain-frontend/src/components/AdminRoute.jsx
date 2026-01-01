import { Navigate, Outlet } from "react-router-dom";

export default function AdminRoute() {
  const token = localStorage.getItem("token");
  const user = JSON.parse(localStorage.getItem("user"));

  // not logged in
  if (!token || !user) {
    return <Navigate to="/login" replace />;
  }

  // not admin
  if (!user.is_admin) {
    return <Navigate to="/" replace />;
  }

  // ✅ REQUIRED for nested routes
  return <Outlet />;
}
