import { Navigate } from "react-router-dom";

export default function AdminRoute({ children }) {
  const admin = localStorage.getItem("is_admin") === "true";
  return admin ? children : <Navigate to="/" />;
}
