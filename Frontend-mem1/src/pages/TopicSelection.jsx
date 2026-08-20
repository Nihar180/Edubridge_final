import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../api/client";
import ChatbotWidget from "../components/ChatbotWidget";
import "./TopicSelection.css";

function TopicSelection({ mode = "learn" }) {
  const { grade, subject } = useParams();
  const navigate = useNavigate();
  const [modules, setModules] = useState([]);
  const [gradeName, setGradeName] = useState(grade || "");
  const [subjectName, setSubjectName] = useState(subject || "");
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([api.get("/units/"), api.get("/modules/"), api.get("/subjects/"), api.get("/profiles/me"), api.get("/grades/")])
      .then(([unitList, moduleList, subjectList, profile, gradeList]) => {
        const selectedSubject = subjectList.find((item) => String(item.id) === subject);
        setSubjectName(selectedSubject?.name || subject);
        setGradeName(gradeList.find((item) => item.id === profile.grade_id)?.name || grade);
        const subjectUnitIds = new Set(
          unitList.filter((unit) => unit.subject_id === selectedSubject?.id).map((unit) => unit.id)
        );
        setModules(moduleList.filter((module) => subjectUnitIds.has(module.unit_id)));
      })
      .catch((requestError) => setError(requestError.message));
  }, [grade, subject]);

  const handleTopicClick = (topic) => {
    navigate(`/${mode}/${grade}/${subject}/${topic.id}`);
  };

  return (
    <div className="topic-container">
      <div className="topic-content">
        <h1>Choose a module</h1>

        <p className="topic-subtitle">
          {gradeName} • {subjectName} • Choose a topic
        </p>

        <div className="topic-options">
          {modules.map((topic) => (
            <button
              key={topic.id}
              onClick={() => handleTopicClick(topic)}
            >
              {topic.title}
            </button>
          ))}
        </div>
        {error && <p>{error}</p>}
      </div>
      <ChatbotWidget />
    </div>
  );
}

export default TopicSelection;