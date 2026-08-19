import { useNavigate, useParams } from "react-router-dom";
import { useState } from "react";
import { quizQuestions } from "../data/quizQuestions";
import "./Quiz.css";

function Quiz() {
  const { grade, subject, topic } = useParams();
  const navigate = useNavigate();

  const questions =
    quizQuestions[`${subject}-${topic}`] || [];

  const [currentQuestion, setCurrentQuestion] = useState(0);

  const [selectedAnswer, setSelectedAnswer] = useState(null);

  const [score, setScore] = useState(0);

  if (questions.length === 0) {
    return (
      <div className="quiz-container">
        <div className="quiz-content">
          <h1>Quiz Not Available</h1>

          <p>
            Questions for this topic are not available yet.
          </p>
        </div>
      </div>
    );
  }

  const question = questions[currentQuestion];

  const handleNext = () => {
    if (selectedAnswer === null) {
      alert("Please select an answer.");
      return;
    }

    let updatedScore = score;

    if (selectedAnswer === question.answer) {
      updatedScore += 1;
      setScore(updatedScore);
    }

    if (currentQuestion === questions.length - 1) {
      navigate(
        `/quiz/${grade}/${subject}/${topic}/result`,
        {
          state: {
            score: updatedScore,
            total: questions.length,
          },
        }
      );

      return;
    }

    setCurrentQuestion(currentQuestion + 1);
    setSelectedAnswer(null);
  };

  const progress =
    ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="quiz-container">
      <div className="quiz-content">

        <div className="quiz-header">

          <p>
            Question {currentQuestion + 1} of{" "}
            {questions.length}
          </p>

          <p>
            Score: {score}
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

          {question.options.map((option, index) => (
            <button
              key={index}
              className={
                selectedAnswer === index
                  ? "selected"
                  : ""
              }
              onClick={() =>
                setSelectedAnswer(index)
              }
            >
              {option}
            </button>
          ))}

        </div>

        <button
          className="quiz-next-button"
          onClick={handleNext}
        >
          {currentQuestion === questions.length - 1
            ? "Submit Quiz"
            : "Next"}
        </button>

      </div>
    </div>
  );
}

export default Quiz;