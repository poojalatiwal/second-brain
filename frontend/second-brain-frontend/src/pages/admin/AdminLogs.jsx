import { useEffect, useState } from "react";
import { getAdminLogs } from "../../api/admin";
import "./Admin.css";

export default function AdminLogs() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    getAdminLogs().then(res => setLogs(res.data));
  }, []);

  return (
    <div className="admin-content">
      <h2>🧾 System Logs</h2>

      <div className="logs">
        {logs.map((log, i) => (
          <div key={i} className="log-item">
            <strong>{log.event}</strong>
            <span>{JSON.stringify(log)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
