import { Outlet } from "react-router-dom";
import AdminNavbar from "../../components/AdminNavbar";
import "./Admin.css";

export default function AdminLayout() {
  return (
    <div className="admin-layout">
      <AdminNavbar />
      <main className="admin-content">
        <Outlet />
      </main>
    </div>
  );
}
