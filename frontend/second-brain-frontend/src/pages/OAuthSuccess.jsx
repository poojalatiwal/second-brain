import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function OAuthSuccess() {
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");

    if (token) {
      localStorage.setItem("token", token);

      // 🔥 IMPORTANT: delay helps React routing
      setTimeout(() => {
        navigate("/", { replace: true });
      }, 100);
    } else {
      navigate("/login", { replace: true });
    }
  }, [navigate]);

  return (
    <div style={{ color: "white", textAlign: "center", marginTop: "40px" }}>
      Logging you in with Google...
    </div>
  );
}
