import { useState } from "react";
import { signup } from "../api/auth";
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

export default function Signup() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const submit = async () => {
    if (!username || !email || !password) {
      alert("All fields required");
      return;
    }

    setLoading(true);

    try {
      await signup({ username, email, password });
      setSuccess(true);

      // auto redirect after 2 seconds
      setTimeout(() => navigate("/login"), 2000);
    } catch (err) {
      alert("Signup failed");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth">
        <h2>Create Account</h2>

        {success && (
          <div className="success-msg">
            ✅ Account created successfully! Redirecting to login…
          </div>
        )}

        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          disabled={success}
        />

        <input
          placeholder="Email address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          disabled={success}
        />

        <div className="password-wrapper">
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={success}
          />
          <button
            type="button"
            className="eye-btn"
            onClick={() => setShowPassword(!showPassword)}
            disabled={success}
          >
            <EyeIcon open={showPassword} />
          </button>
        </div>

        <button className="primary" onClick={submit} disabled={loading || success}>
          {loading ? "Creating..." : "Create Account"}
        </button>

        <div className="auth-divider" />

        <div className="auth-footer">
          Already have an account?
          <Link to="/login">Login</Link>
        </div>
      </div>
    </div>
  );
}
