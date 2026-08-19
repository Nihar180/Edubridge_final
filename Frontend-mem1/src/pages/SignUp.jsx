import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Login.css";

function Signup() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [selectedGrade, setSelectedGrade] = useState("8");

  const grades = ["8", "9", "10"];

  const handleSubmit = (e) => {
    e.preventDefault();
    const userData = {
      username: username.trim() || "Student",
      email: email.trim() || "student@edubridge.org",
      password: password || "123456",
      grade: selectedGrade,
      profilePic: "",
    };
    localStorage.setItem("edubridge_user", JSON.stringify(userData));
    navigate("/home");
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>EduBridge AI Tutor</h1>

        <h2>Sign Up</h2>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <div className="grade-signup-section">
            <label className="grade-signup-label">Select Your Grade</label>
            <div className="grade-signup-buttons">
              {grades.map((grade) => (
                <button
                  key={grade}
                  type="button"
                  className={`grade-signup-btn ${
                    selectedGrade === grade ? "selected" : ""
                  }`}
                  onClick={() => setSelectedGrade(grade)}
                >
                  Grade {grade}
                </button>
              ))}
            </div>
          </div>

          <button type="submit">Sign Up</button>
        </form>

        <p>
          Already have an account? <Link to="/">Login</Link>
        </p>
      </div>
    </div>
  );
}

export default Signup;