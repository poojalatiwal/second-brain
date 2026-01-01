import { useNavigate } from "react-router-dom";
import "../pages/admin/Admin.css";

export default function AdminNavbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <header className="admin-navbar">
      <h3>🧠 SecondBrain • Admin</h3>

      <div className="admin-nav-actions">
        <button onClick={() => navigate("/admin")}>Dashboard</button>
        <button onClick={() => navigate("/admin/users")}>Users</button>
        <button onClick={() => navigate("/admin/logs")}>Logs</button>
        <button className="danger" onClick={logout}>
          Logout
        </button>
      </div>
    </header>
  );
}
