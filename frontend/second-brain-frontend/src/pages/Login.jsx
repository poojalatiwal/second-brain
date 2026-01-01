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

  // ✅ Google Login
  const googleLogin = () => {
    window.location.href = "http://localhost:8000/auth/google";
  };

  // ✅ GitHub Login
  const githubLogin = () => {
    window.location.href = "http://localhost:8000/auth/github";
  };

  const submit = async () => {
    if (!email || !password) {
      alert("Email and password required");
      return;
    }

    try {
      const res = await login({ email, password });

      const {
        access_token,
        refresh_token,
        is_admin,
        id,
        username,
        email: userEmail,
      } = res.data;

      // ✅ Store auth data
      localStorage.setItem("token", access_token);
      localStorage.setItem(
        "user",
        JSON.stringify({
          id,
          username,
          email: userEmail,
          is_admin,
        })
      );

      // ✅ ROLE-BASED REDIRECT
      if (is_admin) {
        navigate("/admin");
      } else {
        navigate("/");
      }
    } catch (err) {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth">
        <h2>Login</h2>

        <input
          placeholder="Email address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <div className="password-wrapper">
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button
            type="button"
            className="eye-btn"
            onClick={() => setShowPassword(!showPassword)}
          >
            <EyeIcon open={showPassword} />
          </button>
        </div>

        <button className="primary" onClick={submit}>
          Login
        </button>

        <div className="auth-divider">Or continue with</div>

        <button className="social-btn" onClick={googleLogin}>
          <img src="/google.svg" alt="Google" />
          Continue with Google
        </button>

        <button className="social-btn" onClick={githubLogin}>
          <img src="/github.svg" alt="GitHub" />
          Continue with GitHub
        </button>

        <div className="auth-footer">
          No account? <Link to="/signup">Create one</Link>
        </div>
      </div>
    </div>
  );
}
