import { useEffect, useState } from "react";
import { getStats } from "../api/admin";

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    getStats().then((res) => setStats(res.data));
  }, []);

  if (!stats) return <div className="container">Loading...</div>;

  return (
    <div className="container">
      <div className="card">
        <h2>Admin Dashboard</h2>
        <p>Total Users: {stats.total_users}</p>
        <p>Total Queries: {stats.total_queries}</p>
        <p>Total Vectors: {stats.total_vectors}</p>
      </div>
    </div>
  );
}
