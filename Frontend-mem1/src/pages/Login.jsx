import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Login.css";

function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();
    const existing = localStorage.getItem("edubridge_user");
    let userData = existing ? JSON.parse(existing) : null;
    if (!userData) {
      userData = {
        username: username.trim() || "Student",
        email: "student@edubridge.org",
        password: password || "123456",
        grade: "8",
        profilePic: "",
      };
      localStorage.setItem("edubridge_user", JSON.stringify(userData));
    } else if (username.trim()) {
      userData.username = username.trim();
      localStorage.setItem("edubridge_user", JSON.stringify(userData));
    }
    navigate("/home");
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

          <button type="submit">Login</button>
        </form>

        <p>
          Don't have an account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;