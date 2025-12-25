import { useState } from "react";
import { signup } from "../api/auth";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const nav = useNavigate();
  const [form, setForm] = useState({ username:"", email:"", password:"" });

  const submit = async () => {
    try {
      const res = await signup(form);
      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("is_admin", res.data.is_admin);
      nav("/chatbot");
    } catch {
      alert("Signup failed");
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Create Account</h2>

        <input placeholder="Username"
          onChange={(e)=>setForm({ ...form, username:e.target.value})} />

        <input placeholder="Email"
          onChange={(e)=>setForm({ ...form, email:e.target.value})} />

        <input type="password" placeholder="Password"
          onChange={(e)=>setForm({ ...form, password:e.target.value})} />

        <button onClick={submit}>Signup</button>
      </div>
    </div>
  );
}
