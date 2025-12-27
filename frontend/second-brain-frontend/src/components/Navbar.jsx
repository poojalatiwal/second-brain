import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <h2>🧠 SecondBrain AI</h2>

      <div className="nav-actions">
        <button onClick={() => navigate("/")}>Home</button>
        <button className="logout" onClick={logout}>
          Logout
        </button>
      </div>
    </nav>
  );
}
