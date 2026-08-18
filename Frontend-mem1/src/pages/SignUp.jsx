import { Link } from "react-router-dom";
import "./Login.css";

function Signup() {
  return (
    <div className="login-container">
      <div className="login-box">
        <h1>EduBridge AI Tutor</h1>

        <h2>Sign Up</h2>

        <input
          type="text"
          placeholder="Enter your name"
        />

        <input
          type="email"
          placeholder="Enter your email"
        />

        <input
          type="password"
          placeholder="Create a password"
        />

        <input
          type="password"
          placeholder="Confirm your password"
        />

        <button>Sign Up</button>

        <p>
            Already have an account? <Link to="/">Login</Link>
        </p>
      </div>
    </div>
  );
}

export default Signup;