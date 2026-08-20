import { Link, useLocation, useParams } from "react-router-dom";
import "./AssessmentResult.css";

function AssessmentResult() {
  const { grade, subject } = useParams();
  const location = useLocation();

  const score = location.state?.score || 0;
  const total = location.state?.total || 0;

  const percentage =
    total > 0
      ? Math.round((score / total) * 100)
      : 0;

  const performance =
    percentage >= 80
      ? "Excellent"
      : percentage >= 60
      ? "Good"
      : percentage >= 40
      ? "Needs Improvement"
      : "Needs More Practice";

  return (
    <div className="assessment-result-container">
      <div className="assessment-result-content">

        <p className="result-subject">
          Grade {grade} • {subject}
        </p>

        <h1>Assessment Complete!</h1>

        <div className="assessment-score">
          {percentage}%
        </div>

        <p className="assessment-score-detail">
          {score} out of {total} correct
        </p>

        <div className="performance-box">
          <h2>{performance}</h2>

          <p>
            Based on your assessment performance,
            here is your current result.
          </p>
        </div>

        <div className="suggestions-box">
          <h2>Suggestions</h2>
          <br />
          {percentage >= 80 ? (
            <ul>
              <li>Keep practicing to maintain your performance.</li>
              <li>Try more challenging questions.</li>
              <li>Explore advanced topics.</li>
            </ul>
          ) : (
            <ul>
              <li>Review the topics you found difficult.</li>
              <li>Practice more questions.</li>
              <li>Revisit the learning content.</li>
            </ul>
          )}
        </div>

        <div className="assessment-result-actions">

          <Link
            to={`/assessment/${grade}/${subject}`}
            className="assessment-result-button"
          >
            Try Again
          </Link>

          <Link
            to={`/dashboard/${grade}`}
            className="assessment-result-button secondary"
          >
            Back to Dashboard
          </Link>

        </div>

      </div>
    </div>
  );
}

export default AssessmentResult;