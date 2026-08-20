import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api, TOKEN_KEY } from "../api/client";
import "./Login.css";

function Signup() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [selectedGrade, setSelectedGrade] = useState("8");
  const [backendGrades, setBackendGrades] = useState([]);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const grades = ["8", "9", "10"];

  useEffect(() => {
    api.get("/grades/").then(setBackendGrades).catch(() => setBackendGrades([]));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const selectedBackendGrade = backendGrades.find(
      (grade) => String(grade.name ?? grade.level ?? grade.grade).replace(/\D/g, "") === selectedGrade || String(grade.id) === selectedGrade
    );

    if (!selectedBackendGrade) {
      setError("The selected grade is not available yet.");
      return;
    }

    setIsSubmitting(true);
    try {
      await api.post("/auth/register", {
        name: username.trim(),
        username: username.trim(),
        email: email.trim(),
        password,
        grade_id: selectedBackendGrade.id,
      });
      const tokenResponse = await api.post("/auth/login", {
        username: username.trim(),
        password,
      });
      localStorage.setItem(TOKEN_KEY, tokenResponse.access_token);
      const profile = await api.get("/profiles/me");
      localStorage.setItem("edubridge_user", JSON.stringify(profile));
      navigate("/home");
    } catch (requestError) {
      setError(requestError.message || "Unable to create your account.");
    } finally {
      setIsSubmitting(false);
    }
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

          {error && <p className="profile-status-msg">{error}</p>}
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Creating account..." : "Sign Up"}
          </button>
        </form>

        <p>
          Already have an account? <Link to="/">Login</Link>
        </p>
      </div>
    </div>
  );
}

export default Signup;