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

  useEffect(() => {
    const loadGrades = async () => {
      try {
        const gradesFromBackend = await api.get("/grades/");

        console.log("Grades received from backend:", gradesFromBackend);

        setBackendGrades(gradesFromBackend);
      } catch (err) {
        console.error("Failed to load grades:", err);
        setError("Unable to load grades. Please make sure the backend is running.");
      }
    };

    loadGrades();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    console.log("Selected grade:", selectedGrade);
    console.log("Backend grades:", backendGrades);

    // Find the backend grade by its name.
    // Backend returns:
    // { id: 1, name: "Grade 8" }
    const selectedBackendGrade = backendGrades.find((grade) => {
      const gradeNumber = String(grade.name || "")
        .replace(/\D/g, "");

      return gradeNumber === selectedGrade;
    });

    console.log("Selected backend grade:", selectedBackendGrade);

    if (!selectedBackendGrade) {
      setError(
        `Grade ${selectedGrade} is not available in the backend.`
      );
      return;
    }

    setIsSubmitting(true);

    try {
      // Register user
      await api.post("/auth/register", {
        name: username.trim(),
        username: username.trim(),
        email: email.trim(),
        password,
        grade_id: selectedBackendGrade.id,
      });

      // Login immediately after registration
      const tokenResponse = await api.post("/auth/login", {
        username: username.trim(),
        password,
      });

      // Save JWT token
      localStorage.setItem(
        TOKEN_KEY,
        tokenResponse.access_token
      );

      // Load user profile
      const profile = await api.get("/profiles/me");

      localStorage.setItem(
        "edubridge_user",
        JSON.stringify(profile)
      );

      // Go to home
      navigate("/home");

    } catch (requestError) {
      console.error("Signup error:", requestError);

      setError(
        requestError.message ||
        "Unable to create your account."
      );

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
            required
          />

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <div className="grade-signup-section">

            <label className="grade-signup-label">
              Select Your Grade
            </label>

            <div className="grade-signup-buttons">

              {["8", "9", "10"].map((grade) => (

                <button
                  key={grade}
                  type="button"
                  className={`grade-signup-btn ${
                    selectedGrade === grade
                      ? "selected"
                      : ""
                  }`}
                  onClick={() => {
                    setSelectedGrade(grade);
                    setError("");
                  }}
                >
                  Grade {grade}
                </button>

              ))}

            </div>

          </div>

          {error && (
            <p className="profile-status-msg">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
          >
            {isSubmitting
              ? "Creating account..."
              : "Sign Up"}
          </button>

        </form>

        <p>
          Already have an account?{" "}
          <Link to="/">
            Login
          </Link>
        </p>

      </div>
    </div>
  );
}

export default Signup;