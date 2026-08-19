import { useState, useEffect } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import "./Home.css";

function Home({ view }) {
  const navigate = useNavigate();
  const location = useLocation();

  const currentView =
    view ||
    (location.pathname === "/profile"
      ? "profile"
      : location.pathname === "/performance"
      ? "performance"
      : "dashboard");

  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("edubridge_user");
    return saved
      ? JSON.parse(saved)
      : {
          username: "Student",
          email: "student@edubridge.org",
          password: "password123",
          grade: "8",
          profilePic: "",
        };
  });

  const [usernameInput, setUsernameInput] = useState(user.username);
  const [passwordInput, setPasswordInput] = useState(user.password);
  const [usernameMsg, setUsernameMsg] = useState("");
  const [passwordMsg, setPasswordMsg] = useState("");
  const [picMsg, setPicMsg] = useState("");

  useEffect(() => {
    setUsernameInput(user.username);
    setPasswordInput(user.password);
  }, [user]);

  const handleUpdateUsername = (e) => {
    e.preventDefault();
    if (!usernameInput.trim()) return;
    const updated = { ...user, username: usernameInput.trim() };
    setUser(updated);
    localStorage.setItem("edubridge_user", JSON.stringify(updated));
    setUsernameMsg("Username updated successfully!");
    setTimeout(() => setUsernameMsg(""), 3000);
  };

  const handleUpdatePassword = (e) => {
    e.preventDefault();
    if (!passwordInput) return;
    const updated = { ...user, password: passwordInput };
    setUser(updated);
    localStorage.setItem("edubridge_user", JSON.stringify(updated));
    setPasswordMsg("Password updated successfully!");
    setTimeout(() => setPasswordMsg(""), 3000);
  };

  const handlePicUpload = (e) => {
    const file = e.target.files && e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const updated = { ...user, profilePic: reader.result };
        setUser(updated);
        localStorage.setItem("edubridge_user", JSON.stringify(updated));
        setPicMsg("Profile picture updated!");
        setTimeout(() => setPicMsg(""), 3000);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="dashboard-layout">
      {/* Sidebar Navigation - EXACTLY 3 OPTIONS */}
      <aside className="sidebar">
        <div className="sidebar-brand">
          <h2>EduBridge</h2>
          <span>AI Tutor</span>
        </div>

        <nav className="sidebar-nav">
          <Link
            to="/home"
            className={`sidebar-link ${currentView === "dashboard" ? "active" : ""}`}
          >
            <span className="sidebar-icon">📊</span>
            <span>Dashboard</span>
          </Link>

          <Link
            to="/performance"
            className={`sidebar-link ${currentView === "performance" ? "active" : ""}`}
          >
            <span className="sidebar-icon">📈</span>
            <span>Performance Analysis</span>
          </Link>

          <Link
            to="/profile"
            className={`sidebar-link ${currentView === "profile" ? "active" : ""}`}
          >
            <span className="sidebar-icon">👤</span>
            <span>Profile</span>
          </Link>
        </nav>
      </aside>

      {/* Main View Container */}
      <main className="dashboard-main">
        {/* 1. DASHBOARD VIEW */}
        {currentView === "dashboard" && (
          <>
            <header className="dashboard-header">
              <div>
                <h1>Welcome back, {user.username}!</h1>
                <p className="dashboard-subtitle">
                  Current Grade: <strong>Grade {user.grade}</strong>
                </p>
              </div>
            </header>

            {/* Basic Performance Summary Cards */}
            <div className="dashboard-cards-grid">
              <div className="dashboard-card">
                <h3>Overall Progress</h3>
                <div className="stat-large">68%</div>
                <div className="progress-bar-container">
                  <div className="progress-bar-fill" style={{ width: "68%" }}></div>
                </div>
                <p className="stat-desc">14 of 20 Lessons Completed</p>
              </div>

              <div className="dashboard-card">
                <h3>Quiz Performance</h3>
                <div className="stat-large">85%</div>
                <p className="stat-highlight">Average Score</p>
                <p className="stat-desc">5 Quizzes Attempted</p>
              </div>

              <div className="dashboard-card">
                <h3>Learning Statistics</h3>
                <div className="stat-list">
                  <div className="stat-item">
                    <span>Weekly Hours</span>
                    <strong>4.5 hrs</strong>
                  </div>
                  <div className="stat-item">
                    <span>Topics Mastered</span>
                    <strong>8 Topics</strong>
                  </div>
                </div>
              </div>
            </div>

            {/* THREE MAIN DASHBOARD CONTENT OPTIONS: [ Learn ] [ Quiz ] [ Assignment ] */}
            <div className="dashboard-section">
              <h2>What would you like to do?</h2>
              <div className="dashboard-options-grid">
                <div
                  className="dashboard-action-card"
                  onClick={() => navigate(`/learn/${user.grade}`)}
                >
                  <div className="action-card-header">
                    <span className="action-icon">📖</span>
                    <h3>Learn</h3>
                  </div>
                  <p>Study topics and learning materials</p>
                  <button
                    className="start-button"
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/learn/${user.grade}`);
                    }}
                  >
                    Start Learning
                  </button>
                </div>

                <div
                  className="dashboard-action-card"
                  onClick={() => navigate(`/quiz/${user.grade}`)}
                >
                  <div className="action-card-header">
                    <span className="action-icon">📝</span>
                    <h3>Quiz</h3>
                  </div>
                  <p>Practice and test your knowledge</p>
                  <button
                    className="start-button"
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/quiz/${user.grade}`);
                    }}
                  >
                    Take Quiz
                  </button>
                </div>

                <div
                  className="dashboard-action-card"
                  onClick={() => navigate(`/assessment/${user.grade}`)}
                >
                  <div className="action-card-header">
                    <span className="action-icon">🎓</span>
                    <h3>Assignment</h3>
                  </div>
                  <p>Check your overall understanding</p>
                  <button
                    className="start-button"
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/assessment/${user.grade}`);
                    }}
                  >
                    Start Assignment
                  </button>
                </div>
              </div>
            </div>
          </>
        )}

        {/* 2. PERFORMANCE ANALYSIS VIEW */}
        {currentView === "performance" && (
          <>
            <header className="dashboard-header">
              <div>
                <h1>Performance Analysis</h1>
                <p className="dashboard-subtitle">
                  Student Performance Overview • <strong>Grade {user.grade}</strong>
                </p>
              </div>
            </header>

            <div className="performance-summary-grid">
              <div className="dashboard-card">
                <h3>Overall Progress</h3>
                <div className="stat-large">72%</div>
                <p className="stat-desc">Completed across Grade {user.grade}</p>
              </div>

              <div className="dashboard-card">
                <h3>Lessons Completed</h3>
                <div className="stat-large">15</div>
                <p className="stat-desc">Out of 21 total topics</p>
              </div>

              <div className="dashboard-card">
                <h3>Quiz Performance</h3>
                <div className="stat-large">84%</div>
                <p className="stat-desc">Average Score across 8 quizzes</p>
              </div>

              <div className="dashboard-card">
                <h3>Assignment Score</h3>
                <div className="stat-large">86%</div>
                <p className="stat-desc">2 Assignments Completed</p>
              </div>
            </div>

            <div className="dashboard-section performance-section">
              <h2>Subject Learning Progress</h2>
              <div className="subject-perf-list">
                <div className="subject-perf-item">
                  <div className="subject-perf-info">
                    <span className="subject-perf-name">Mathematics</span>
                    <span className="subject-perf-stats">6 / 8 Topics • Avg Score: <strong>88%</strong></span>
                  </div>
                  <div className="progress-bar-container">
                    <div className="progress-bar-fill" style={{ width: "80%" }}></div>
                  </div>
                </div>

                <div className="subject-perf-item">
                  <div className="subject-perf-info">
                    <span className="subject-perf-name">Science</span>
                    <span className="subject-perf-stats">5 / 7 Topics • Avg Score: <strong>82%</strong></span>
                  </div>
                  <div className="progress-bar-container">
                    <div className="progress-bar-fill" style={{ width: "70%" }}></div>
                  </div>
                </div>

                <div className="subject-perf-item">
                  <div className="subject-perf-info">
                    <span className="subject-perf-name">English</span>
                    <span className="subject-perf-stats">4 / 6 Topics • Avg Score: <strong>78%</strong></span>
                  </div>
                  <div className="progress-bar-container">
                    <div className="progress-bar-fill" style={{ width: "65%" }}></div>
                  </div>
                </div>
              </div>
            </div>

            <div className="dashboard-section performance-section">
              <h2>Recent Quiz & Assignment Results</h2>
              <div className="quiz-history-list">
                <div className="quiz-history-row">
                  <div>
                    <h4 className="quiz-title">Algebra: Linear Equations (Quiz)</h4>
                    <span className="quiz-date">Yesterday</span>
                  </div>
                  <div className="quiz-score-box">
                    <span className="quiz-score">90%</span>
                    <span className="quiz-status-badge">Passed</span>
                  </div>
                </div>

                <div className="quiz-history-row">
                  <div>
                    <h4 className="quiz-title">Grade {user.grade} Science Assessment (Assignment)</h4>
                    <span className="quiz-date">2 days ago</span>
                  </div>
                  <div className="quiz-score-box">
                    <span className="quiz-score">86%</span>
                    <span className="quiz-status-badge">Completed</span>
                  </div>
                </div>

                <div className="quiz-history-row">
                  <div>
                    <h4 className="quiz-title">Physics: Force & Motion (Quiz)</h4>
                    <span className="quiz-date">3 days ago</span>
                  </div>
                  <div className="quiz-score-box">
                    <span className="quiz-score">85%</span>
                    <span className="quiz-status-badge">Passed</span>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}

        {/* 3. PROFILE VIEW */}
        {currentView === "profile" && (
          <>
            <header className="dashboard-header">
              <div>
                <h1>Student Profile</h1>
                <p className="dashboard-subtitle">Manage your account details</p>
              </div>
            </header>

            <div className="profile-container-card">
              {/* Profile Picture Upload & Display */}
              <div className="profile-picture-section">
                <div className="avatar-preview">
                  {user.profilePic ? (
                    <img src={user.profilePic} alt="Profile Avatar" className="avatar-img" />
                  ) : (
                    <div className="avatar-placeholder">
                      {user.username ? user.username.charAt(0).toUpperCase() : "S"}
                    </div>
                  )}
                </div>

                <div className="avatar-actions">
                  <input
                    type="file"
                    accept="image/*"
                    id="profile-pic-upload"
                    style={{ display: "none" }}
                    onChange={handlePicUpload}
                  />
                  <label htmlFor="profile-pic-upload" className="profile-btn-small">
                    Change Picture
                  </label>
                  {picMsg && <span className="profile-status-msg">{picMsg}</span>}
                </div>
              </div>

              {/* Profile Fields List */}
              <div className="profile-fields-list">
                {/* Username with specific Update button */}
                <div className="profile-field-group">
                  <label className="profile-label">Username</label>
                  <div className="profile-input-inline">
                    <input
                      type="text"
                      className="profile-input"
                      value={usernameInput}
                      onChange={(e) => setUsernameInput(e.target.value)}
                    />
                    <button
                      type="button"
                      className="profile-btn-small"
                      onClick={handleUpdateUsername}
                    >
                      Update Username
                    </button>
                  </div>
                  {usernameMsg && <span className="profile-status-msg">{usernameMsg}</span>}
                </div>

                {/* Password with specific Update button */}
                <div className="profile-field-group">
                  <label className="profile-label">Password</label>
                  <div className="profile-input-inline">
                    <input
                      type="password"
                      className="profile-input"
                      value={passwordInput}
                      onChange={(e) => setPasswordInput(e.target.value)}
                    />
                    <button
                      type="button"
                      className="profile-btn-small"
                      onClick={handleUpdatePassword}
                    >
                      Update Password
                    </button>
                  </div>
                  {passwordMsg && <span className="profile-status-msg">{passwordMsg}</span>}
                </div>

                {/* Email - READ-ONLY */}
                <div className="profile-field-group">
                  <label className="profile-label">
                    Email <span className="readonly-tag">(Cannot be edited)</span>
                  </label>
                  <input
                    type="email"
                    className="profile-input disabled"
                    value={user.email}
                    disabled
                  />
                </div>

                {/* Grade - READ-ONLY */}
                <div className="profile-field-group">
                  <label className="profile-label">
                    Grade <span className="readonly-tag">(Cannot be edited from Profile)</span>
                  </label>
                  <input
                    type="text"
                    className="profile-input disabled"
                    value={`Grade ${user.grade}`}
                    disabled
                  />
                </div>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default Home;