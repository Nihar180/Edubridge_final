import { useNavigate, useParams } from "react-router-dom";
import { subjects } from "../data/subjects";
import ChatbotWidget from "../components/ChatbotWidget";
import "./SubjectSelection.css";

function SubjectSelection({ mode = "learn" }) {
  const { grade } = useParams();
  const navigate = useNavigate();

  const selectedGrade = grade || "8";
  const gradeSubjects = subjects[selectedGrade] || subjects["8"] || [];

  const handleSubjectClick = (subject) => {
    navigate(`/${mode}/${selectedGrade}/${subject}`);
  };

  return (
    <div className="subject-container">
      <div className="subject-content">
        <h1>Grade {selectedGrade}</h1>

        <p className="subject-subtitle">
          Choose a subject to continue
        </p>

        <div className="subject-options">
          {gradeSubjects.map((subject) => (
            <button
              key={subject}
              onClick={() => handleSubjectClick(subject)}
            >
              {subject}
            </button>
          ))}
        </div>
      </div>
      <ChatbotWidget />
    </div>
  );
}

export default SubjectSelection;