import { useParams } from "react-router-dom";
import { learningContent } from "../data/learningContent";
import ChatbotWidget from "../components/ChatbotWidget";
import "./LearningContent.css";

function LearningContent() {
  const { grade, subject, topic } = useParams();

  const content = learningContent[`${subject}-${topic}`];

  if (!content) {
    return (
      <div className="learning-container">
        <div className="learning-content">
          <h1>Content Not Available</h1>

          <p>
            Learning content for this topic is not available yet.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="learning-container">
      <div className="learning-content">

        <p className="learning-breadcrumb">
          Grade {grade} • {subject}
        </p>

        <h1>{content.title}</h1>

        <section className="learning-section">
          <h2>Explanation</h2>

          <p>{content.explanation}</p>
        </section>

        <section className="learning-section">
          <h2>Examples</h2>

          {content.examples.map((example, index) => (
            <div
              className="example-box"
              key={index}
            >
              {example}
            </div>
          ))}
        </section>

        <section className="learning-section">
          <h2>Key Points</h2>

          <ul>
            {content.keyPoints.map((point, index) => (
              <li key={index}>
                {point}
              </li>
            ))}
          </ul>
        </section>

      </div>
      <ChatbotWidget />
    </div>
  );
}

export default LearningContent;