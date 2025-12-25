import { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ThemeContext } from "../ThemeContext";

export default function Navbar() {
  const { theme, setTheme } = useContext(ThemeContext);
  const nav = useNavigate();

  const logout = () => {
    localStorage.clear();
    nav("/login");
  };

  return (
    <div className="navbar">
      <div>
        <Link to="/chatbot">Chatbot</Link>
        <Link to="/memory">Memory</Link>
        <Link to="/ingest">Ingest</Link>
        <Link to="/hybrid">Hybrid Search</Link>

        {localStorage.getItem("is_admin") === "true" && (
          <>
            <Link to="/admin">Admin</Link>
            <Link to="/admin/users">Users</Link>
            <Link to="/admin/logs">Logs</Link>
          </>
        )}
      </div>

      <div>
        <button 
          style={{ width: "auto", marginRight: "10px" }}
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        >
          {theme === "dark" ? "☀ Light" : "🌙 Dark"}
        </button>

        <button style={{ width: "auto" }} onClick={logout}>Logout</button>
      </div>
    </div>
  );
}
