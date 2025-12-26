import { getStats } from "../api/admin";
import { useEffect, useState } from "react";

export default function AdminDashboard() {
  const [stats, setStats] = useState({});

  useEffect(()=>{
    getStats().then(r=>setStats(r.data));
  },[]);

  return (
    <>
      <h2>Admin Dashboard</h2>
      <pre>{JSON.stringify(stats, null, 2)}</pre>
    </>
  );
}
