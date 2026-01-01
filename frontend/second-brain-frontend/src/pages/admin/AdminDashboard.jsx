import { useEffect, useState } from "react";
import { getAdminStats } from "../../api/admin";
import { useNavigate } from "react-router-dom";
import "./Admin.css";

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    getAdminStats().then(res => setStats(res.data));
  }, []);

  if (!stats) return <p className="muted">Loading dashboard...</p>;

  return (
    <>
      <div className="admin-header-card">
        <h2>🛠 Admin Dashboard</h2>
        <p className="muted">System overview</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card hover-card" onClick={() => navigate("/admin/users")}>
          <h4>Total Users</h4>
          <span>{stats.total_users}</span>
        </div>

        <div className="stat-card hover-card">
          <h4>Admin Users</h4>
          <span>{stats.admin_users}</span>
        </div>

        <div className="stat-card hover-card">
          <h4>Memory Vectors</h4>
          <span>{stats.total_vectors}</span>
        </div>

        <div className="stat-card hover-card">
          <h4>Documents</h4>
          <span>{stats.estimated_docs}</span>
        </div>
      </div>
    </>
  );
}
