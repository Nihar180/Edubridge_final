import { Link, useLocation, useParams } from "react-router-dom";
import "./QuizResult.css";

function QuizResult() {
  const { grade } = useParams();
  const { subject } = useParams();
  const location = useLocation();

  const score = location.state?.score || 0;
  const total = location.state?.total_marks || 0;
  const percentage = Math.round(location.state?.percentage || 0);

  return (
    <div className="result-container">
      <div className="result-content">

        <h1>Quiz Completed!</h1>

        <div className="result-score">
          <span>{score}</span>
          <span> / {total}</span>
        </div>

        <p className="result-percentage">
          {percentage}%
        </p>

        <p>
          You scored {score} out of {total} marks.
        </p>

        <div className="result-actions">

          <Link
            to={`/quiz/${grade}/${subject}`}
            className="result-button"
          >
            Try Again
          </Link>

          <Link
            to={`/dashboard/${grade}`}
            className="result-button secondary"
          >
            Back to Dashboard
          </Link>

        </div>

      </div>
    </div>
  );
}

export default QuizResult;