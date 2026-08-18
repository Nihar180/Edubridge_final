import { Link, useNavigate } from "react-router-dom";
import "./Login.css";

function Login() {
    const navigate = useNavigate();
  return (
    <div className="login-container">
      <div className="login-box">
        <h1>EduBridge AI Tutor</h1>

        <h2>Login</h2>

        <input
          type="email"
          placeholder="Enter your email"
        />

        <input
          type="password"
          placeholder="Enter your password"
        />

        <button onClick={() => navigate("/home")}>
            Login
        </button>

        <p>
            Don't have an account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;