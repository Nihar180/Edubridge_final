import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api, TOKEN_KEY } from "../api/client";
import "./Login.css";

function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      const tokenResponse = await api.post("/auth/login", {
        username: username.trim(),
        password,
      });
      localStorage.setItem(TOKEN_KEY, tokenResponse.access_token);
      const profile = await api.get("/profiles/me");
      localStorage.setItem("edubridge_user", JSON.stringify(profile));
      navigate("/home");
    } catch (requestError) {
      setError(
        requestError.status
          ? `${requestError.message} (${requestError.status})`
          : requestError.message || "Unable to log in."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>EduBridge AI Tutor</h1>

        <h2>Login</h2>

        <form onSubmit={handleLogin}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          {error && <p className="profile-status-msg">{error}</p>}
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Logging in..." : "Login"}
          </button>
        </form>

        <p>
          Don't have an account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;