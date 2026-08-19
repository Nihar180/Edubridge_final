import { useNavigate, useParams } from "react-router-dom";
import { topics } from "../data/topics";
import ChatbotWidget from "../components/ChatbotWidget";
import "./TopicSelection.css";

function TopicSelection({ mode = "learn" }) {
  const { grade, subject } = useParams();
  const navigate = useNavigate();

  const subjectTopics = topics[subject] || [];

  const handleTopicClick = (topic) => {
    navigate(`/${mode}/${grade}/${subject}/${topic}`);
  };

  return (
    <div className="topic-container">
      <div className="topic-content">
        <h1>{subject}</h1>

        <p className="topic-subtitle">
          Grade {grade} • Choose a topic
        </p>

        <div className="topic-options">
          {subjectTopics.map((topic) => (
            <button
              key={topic}
              onClick={() => handleTopicClick(topic)}
            >
              {topic}
            </button>
          ))}
        </div>
      </div>
      <ChatbotWidget />
    </div>
  );
}

export default TopicSelection;