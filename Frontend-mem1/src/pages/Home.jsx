import { Link } from "react-router-dom";
import "./Home.css";

function Home() {
  return (
    <div className="home-container">
      <div className="home-content">
        <h1>Welcome to EduBridge AI Tutor</h1>

        <p className="home-subtitle">
          Your personalized space to learn, practice, and improve.
        </p>

        <Link to="/grades">
          <button className="start-button">Start Learning</button>
        </Link>
      </div>
    </div>
  );
}

export default Home;