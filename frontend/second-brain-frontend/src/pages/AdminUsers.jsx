import { useEffect, useState } from "react";
import { getUsers } from "../api/admin";

export default function AdminUsers() {
  const [users, setUsers] = useState([]);

  useEffect(()=>{
    getUsers().then(res => setUsers(res.data));
  }, []);

  return (
    <div className="container">
      <div className="card">
        <h2>All Users</h2>

        {users.map(u=>(
          <div key={u.id} style={{padding:"10px 0", borderBottom:"1px solid var(--border)"}}>
            <strong>{u.username}</strong> — {u.email}
          </div>
        ))}
      </div>
    </div>
  );
}
