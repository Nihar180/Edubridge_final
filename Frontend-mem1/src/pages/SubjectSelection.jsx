import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../api/client";
import ChatbotWidget from "../components/ChatbotWidget";
import "./SubjectSelection.css";

function SubjectSelection({ mode = "learn" }) {
  const { grade } = useParams();
  const navigate = useNavigate();
  const [subjects, setSubjects] = useState([]);
  const [gradeName, setGradeName] = useState("");
  const [error, setError] = useState("");

  const selectedGrade = grade || "8";

  useEffect(() => {
    Promise.all([api.get("/subjects/"), api.get("/profiles/me"), api.get("/grades/")])
      .then(([subjectList, profile, gradeList]) => {
        setSubjects(subjectList.filter((subject) => subject.grade_id === profile.grade_id));
        setGradeName(gradeList.find((item) => item.id === profile.grade_id)?.name || "");
      })
      .catch((requestError) => setError(requestError.message));
  }, []);

  const handleSubjectClick = (subject) => {
    navigate(`/${mode}/${selectedGrade}/${subject.id}`);
  };

  return (
    <div className="subject-container">
      <div className="subject-content">
        <h1>{gradeName || "Loading grade..."}</h1>

        <p className="subject-subtitle">
          Choose a subject to continue
        </p>

        <div className="subject-options">
          {subjects.map((subject) => (
            <button
              key={subject.id}
              onClick={() => handleSubjectClick(subject)}
            >
              {subject.name}
            </button>
          ))}
        </div>
        {error && <p>{error}</p>}
      </div>
      <ChatbotWidget />
    </div>
  );
}

export default SubjectSelection;