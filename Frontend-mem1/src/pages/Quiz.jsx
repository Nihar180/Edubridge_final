import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { api } from "../api/client";
import "./Quiz.css";

function Quiz() {
  const { grade, subject, topic } = useParams();
  const navigate = useNavigate();

  const [quiz, setQuiz] = useState(null);
  const [attemptId, setAttemptId] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    api.get(`/quizzes/module/${topic}`)
      .then(async (quizzes) => {
        if (!quizzes.length) {
          setQuiz({ questions: [] });
          return;
        }
        const started = await api.post(`/quizzes/${quizzes[0].id}/start`);
        setAttemptId(started.attempt_id);
        setQuiz({ ...quizzes[0], questions: started.questions });
      })
      .catch((requestError) => setError(requestError.message));
  }, [topic]);

  if (error || (quiz && quiz.questions.length === 0)) {
    return (
      <div className="quiz-container">
        <div className="quiz-content">
          <h1>{error ? "Unable to load quiz" : "Quiz Not Available"}</h1>
          <p>{error || "Questions for this module are not available yet."}</p>
        </div>
      </div>
    );
  }

  if (!quiz) return <div className="quiz-container"><div className="quiz-content"><p>Loading quiz...</p></div></div>;

  const question = quiz.questions[currentQuestion];

  const handleNext = async () => {
    if (answers[question.id] === undefined) {
      alert("Please select an answer.");
      return;
    }

    if (currentQuestion === quiz.questions.length - 1) {
      setIsSubmitting(true);
      try {
        const result = await api.post(`/quizzes/${quiz.id}/submit`, {
          attempt_id: attemptId,
          answers: quiz.questions.map((item) => ({
            question_id: item.id,
            selected_option_id: answers[item.id] ?? null,
          })),
        });
        navigate(`/quiz/${grade}/${subject}/${topic}/result`, { state: result });
      } catch (requestError) {
        setError(requestError.message);
      } finally {
        setIsSubmitting(false);
      }

      return;
    }

    setCurrentQuestion(currentQuestion + 1);
  };

  const progress =
    ((currentQuestion + 1) / quiz.questions.length) * 100;

  return (
    <div className="quiz-container">
      <div className="quiz-content">

        <div className="quiz-header">

          <p>
            Question {currentQuestion + 1} of {quiz.questions.length}
          </p>

        </div>

        <div className="quiz-progress">
          <div
            className="quiz-progress-bar"
            style={{ width: `${progress}%` }}
          ></div>
        </div>

        <h1>{question.question}</h1>

        <div className="quiz-options">

          {question.options.map((option) => (
            <button
              key={option.id}
              className={answers[question.id] === option.id ? "selected" : ""}
              onClick={() =>
                setAnswers((previous) => ({ ...previous, [question.id]: option.id }))
              }
            >
              {option.option_text}
            </button>
          ))}

        </div>

        <button
          className="quiz-next-button"
          disabled={isSubmitting}
          onClick={handleNext}
        >
          {isSubmitting
            ? "Submitting..."
            : currentQuestion === quiz.questions.length - 1
            ? "Submit Quiz"
            : "Next"}
        </button>

      </div>
    </div>
  );
}

export default Quiz;