import { useState } from "react";
import { login } from "../api/auth";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const nav = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });

  const handleLogin = async () => {
    try {
      const res = await login(form);
      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("is_admin", res.data.is_admin);
      nav("/chatbot");
    } catch (e) {
      alert("Invalid login");
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Login</h2>

        <input
          placeholder="Email"
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />

        <input
          placeholder="Password"
          type="password"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />

        <button onClick={handleLogin}>Login</button>
      </div>
    </div>
  );
}
