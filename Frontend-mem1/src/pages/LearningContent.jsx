import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api/client";
import ChatbotWidget from "../components/ChatbotWidget";
import "./LearningContent.css";

function structureContent(contentText) {
  const sections = [];
  let paragraphLines = [];
  let activeSection = null;

  const flushParagraph = () => {
    if (paragraphLines.length > 0) {
      const paragraph = paragraphLines.join(" ").trim();
      if (paragraph) {
        if (activeSection) {
          activeSection.paragraphs.push(paragraph);
        } else {
          sections.push({ heading: "Explanation", paragraphs: [paragraph], items: [] });
        }
      }
      paragraphLines = [];
    }
  };

  contentText.split(/\r?\n/).forEach((rawLine) => {
    const line = rawLine.trim();
    if (!line) {
      flushParagraph();
      return;
    }

    const headingMatch = line.match(/^(.+):$/);
    if (headingMatch) {
      flushParagraph();
      activeSection = { heading: headingMatch[1], paragraphs: [], items: [] };
      sections.push(activeSection);
      return;
    }

    const bulletMatch = line.match(/^[-*]\s+(.+)$/);
    if (bulletMatch && activeSection) {
      activeSection.items.push(bulletMatch[1]);
      return;
    }

    paragraphLines.push(bulletMatch ? bulletMatch[1] : line);
  });
  flushParagraph();

  return sections;
}

function LearningContent() {
  const { grade, subject, topic } = useParams();
  const [contents, setContents] = useState([]);
  const [error, setError] = useState("");
  const [breadcrumb, setBreadcrumb] = useState(`Grade ${grade} • ${subject}`);
  const [completingContentId, setCompletingContentId] = useState(null);
  const [completionMessage, setCompletionMessage] = useState("");
  const [completionError, setCompletionError] = useState("");

  useEffect(() => {
    Promise.all([
      api.get(`/learning-contents/module/${topic}`),
      api.get("/profiles/me"),
      api.get("/grades/"),
      api.get("/subjects/"),
    ])
      .then(([contentList, profile, gradeList, subjectList]) => {
        setContents(contentList);
        const gradeName = gradeList.find((item) => item.id === profile.grade_id)?.name || grade;
        const subjectName = subjectList.find((item) => String(item.id) === subject)?.name || subject;
        setBreadcrumb(`${gradeName} • ${subjectName}`);
      })
      .catch((requestError) => setError(requestError.message));
  }, [grade, subject, topic]);

  if (error) {
    return (
      <div className="learning-container">
        <div className="learning-content">
          <h1>Unable to load content</h1>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="learning-container">
      <div className="learning-content">

        <p className="learning-breadcrumb">
          {breadcrumb}
        </p>

        {contents.length === 0 && <p>Learning content for this module is not available yet.</p>}
        {contents.map((content) => (
          <section className="learning-section" key={content.id}>
            <h1>{content.title}</h1>
            {content.content ? (
              structureContent(content.content).map((section, sectionIndex) => (
                <section className="learning-section" key={`${content.id}-${section.heading}-${sectionIndex}`}>
                  <h2>{section.heading}</h2>
                  {section.paragraphs.map((paragraph, paragraphIndex) => (
                    <p key={`${content.id}-paragraph-${paragraphIndex}`}>{paragraph}</p>
                  ))}
                  {section.items.length > 0 && (
                    section.heading.toLowerCase().includes("example") ? (
                      section.items.map((item, itemIndex) => (
                        <div className="example-box" key={`${content.id}-example-${itemIndex}`}>
                          {item}
                        </div>
                      ))
                    ) : (
                      <ul>
                        {section.items.map((item, itemIndex) => (
                          <li key={`${content.id}-item-${itemIndex}`}>{item}</li>
                        ))}
                      </ul>
                    )
                  )}
                </section>
              ))
            ) : (
              <p>This content does not have a written explanation.</p>
            )}
            {content.media_url && <a href={content.media_url} target="_blank" rel="noreferrer">Open resource</a>}
            <button
              type="button"
              className="start-button"
              disabled={content.is_completed || completingContentId === content.id}
              onClick={async () => {
                setCompletionError("");
                setCompletionMessage("");
                setCompletingContentId(content.id);
                try {
                  const completion = await api.post(`/learning-contents/${content.id}/complete`);
                  setContents((previous) => previous.map((item) => (
                    item.id === content.id ? { ...item, is_completed: true } : item
                  )));
                  setCompletionMessage(completion.message || "Learning content marked as completed.");
                } catch (requestError) {
                  setCompletionError(requestError.message || "Unable to mark this content as completed.");
                } finally {
                  setCompletingContentId(null);
                }
              }}
            >
              {completingContentId === content.id
                ? "Marking as completed..."
                : content.is_completed
                ? "Completed"
                : "Mark as completed"}
            </button>
            {completionMessage && <p className="profile-status-msg">{completionMessage}</p>}
            {completionError && <p className="profile-status-msg">{completionError}</p>}
          </section>
        ))}

      </div>
      <ChatbotWidget />
    </div>
  );
}

export default LearningContent;