import { useEffect, useState } from "react";
import { getAdminStats } from "../../api/admin";
import "./Admin.css";

export default function AdminStats() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    getAdminStats().then(res => setStats(res.data));
  }, []);

  if (!stats) return <p className="muted">Loading stats...</p>;

  return (
    <div className="admin-content">
      <h2>📊 System Overview</h2>

      <div className="stats-grid">
        <div className="stat-card">
          <h4>Total Users</h4>
          <span>{stats.total_users}</span>
        </div>

        <div className="stat-card">
          <h4>Admin Users</h4>
          <span>{stats.admin_users}</span>
        </div>

        <div className="stat-card">
          <h4>Memory Vectors</h4>
          <span>{stats.total_vectors}</span>
        </div>

        <div className="stat-card">
          <h4>Documents</h4>
          <span>{stats.estimated_docs}</span>
        </div>
      </div>
    </div>
  );
}
