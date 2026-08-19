import { useNavigate, useParams } from "react-router-dom";
import { useState } from "react";
import { assessmentQuestions } from "../data/assessmentQuestions";
import "./Assessment.css";

function Assessment() {
  const { grade, subject } = useParams();
  const navigate = useNavigate();

  const questions = assessmentQuestions[subject] || [];

  const [currentQuestion, setCurrentQuestion] = useState(0);

  const [selectedAnswer, setSelectedAnswer] = useState(null);

  const [score, setScore] = useState(0);

  if (questions.length === 0) {
    return (
      <div className="assessment-container">
        <div className="assessment-content">
          <h1>Assessment Not Available</h1>

          <p>
            Assessment questions for this subject
            are not available yet.
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
        `/assessment/${grade}/${subject}/result`,
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
    <div className="assessment-container">
      <div className="assessment-content">

        <div className="assessment-header">

          <div>
            <p>
              Question {currentQuestion + 1} of{" "}
              {questions.length}
            </p>
          </div>

          <span
            className={`difficulty ${question.difficulty.toLowerCase()}`}
          >
            {question.difficulty}
          </span>

        </div>

        <div className="assessment-progress">
          <div
            className="assessment-progress-bar"
            style={{ width: `${progress}%` }}
          ></div>
        </div>

        <h1>{question.question}</h1>

        <div className="assessment-options">

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
          className="assessment-next-button"
          onClick={handleNext}
        >
          {currentQuestion === questions.length - 1
            ? "Submit Assessment"
            : "Next"}
        </button>

      </div>
    </div>
  );
}

export default Assessment;