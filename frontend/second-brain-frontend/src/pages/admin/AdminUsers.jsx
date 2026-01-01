import { useEffect, useState } from "react";
import { getAdminUsers } from "../../api/admin";
import "./Admin.css";

export default function AdminUsers() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    getAdminUsers().then(res => setUsers(res.data));
  }, []);

  return (
    <div className="admin-content">
      <h2>👥 Manage Users</h2>

      <table className="admin-table">
        <thead>
          <tr>
            <th>Email</th>
            <th>Username</th>
            <th>Role</th>
          </tr>
        </thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id}>
              <td>{u.email}</td>
              <td>{u.username}</td>
              <td>{u.is_admin ? "Admin" : "User"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
