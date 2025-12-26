import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <nav className="nav">
      <h2>🧠 SecondBrain AI</h2>
      <div>
        <Link to="/">Home</Link>
        <button onClick={logout}>Logout</button>
      </div>
    </nav>
  );
}
