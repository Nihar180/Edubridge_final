import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/SignUp";
import Home from "./pages/Home";
import GradeDashboard from "./pages/GradeDashboard";
import SubjectSelection from "./pages/SubjectSelection";
import TopicSelection from "./pages/TopicSelection";
import LearningContent from "./pages/LearningContent";
import Quiz from "./pages/Quiz";
import QuizResult from "./pages/QuizResult";
import Assessment from "./pages/Assessment";
import AssessmentResult from "./pages/AssessmentResult";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/home" element={<Home view="dashboard" />} />
        <Route path="/profile" element={<Home view="profile" />} />
        <Route path="/performance" element={<Home view="performance" />} />
        <Route path="/dashboard/:grade" element={<GradeDashboard />} />
        <Route path="/learn/:grade" element={<SubjectSelection mode="learn" />} />
        <Route path="/quiz/:grade" element={<SubjectSelection mode="quiz" />} />
        <Route path="/learn/:grade/:subject" element={<TopicSelection mode="learn" />} />
        <Route path="/quiz/:grade/:subject" element={<TopicSelection mode="quiz" />} />
        <Route path="/learn/:grade/:subject/:topic" element={<LearningContent />} />
        <Route path="/quiz/:grade/:subject/:topic" element={<Quiz />} />
        <Route path="/quiz/:grade/:subject/:topic/result" element={<QuizResult />} />
        <Route path="/assessment/:grade" element={<SubjectSelection mode="assessment" />} />
        <Route path="/assessment/:grade/:subject" element={<Assessment />} />
        <Route path="/assessment/:grade/:subject/result" element={<AssessmentResult />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
