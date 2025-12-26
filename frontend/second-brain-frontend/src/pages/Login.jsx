import { useState } from "react";
import { login } from "../api/auth";
import { Link, useNavigate } from "react-router-dom";

/* Eye Icon */
function EyeIcon({ open }) {
  return open ? (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8S1 12 1 12z" stroke="currentColor" strokeWidth="2" />
      <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2" />
    </svg>
  ) : (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
      <path d="M3 3l18 18" stroke="currentColor" strokeWidth="2" />
      <path d="M10.6 10.6a3 3 0 004.2 4.2" stroke="currentColor" strokeWidth="2" />
      <path d="M9.9 4.2A10.9 10.9 0 0121 12c-1.7 3.6-5.1 6-9 6a9.6 9.6 0 01-3.6-.7" stroke="currentColor" strokeWidth="2" />
    </svg>
  );
}

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const navigate = useNavigate();

  const submit = async () => {
    if (!email || !password) return alert("Email and password required");

    try {
      const res = await login({ email, password });
      localStorage.setItem("token", res.data.access_token);
      navigate("/");
    } catch (err) {
      alert("Invalid credentials");
      console.error(err);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth">
        <h2>LogIn</h2>

        <input placeholder="Email address" value={email} onChange={(e) => setEmail(e.target.value)} />

        <div className="password-wrapper">
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="button" className="eye-btn" onClick={() => setShowPassword(!showPassword)}>
            <EyeIcon open={showPassword} />
          </button>
        </div>

        <button className="primary" onClick={submit}>Login</button>

        <div className="auth-divider" />

        <div className="auth-footer">
          No account?
          <Link to="/signup">Create one</Link>
        </div>
      </div>
    </div>
  );
}
