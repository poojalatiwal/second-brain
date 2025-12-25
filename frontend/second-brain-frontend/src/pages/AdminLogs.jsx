import { useEffect, useState } from "react";
import { getLogs } from "../api/admin";

export default function AdminLogs() {
  const [logs, setLogs] = useState([]);

  useEffect(()=>{
    getLogs().then(res => setLogs(res.data));
  }, []);

  return (
    <div className="container">
      <div className="card">
        <h2>System Logs</h2>

        {logs.map((l, i)=>(
          <div key={i} style={{padding:"10px 0", borderBottom:"1px solid var(--border)"}}>
            <strong>User:</strong> {l.user_id}  
            <br/>
            <strong>Action:</strong> {l.action}
          </div>
        ))}
      </div>
    </div>
  );
}
