import "./GradeSelection.css";

function GradeSelection() {
  return (
    <div className="grade-container">
      <h1>Choose Your Grade</h1>

      <p>Select your grade to start learning</p>

      <div className="grade-options">
        <button>Grade 7</button>
        <button>Grade 8</button>
        <button>Grade 9</button>
        <button>Grade 10</button>
      </div>
    </div>
  );
}

export default GradeSelection;