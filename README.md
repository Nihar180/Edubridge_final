# 🎓 EduBridge AI Tutor

> An AI-powered personalized learning platform that helps students Learn, Ask, Practice, Assess, and Improve.

---

## 🎥 Project Demo

### ▶️ Watch the Complete Project Demo

🎬 [Watch EduBridge AI Tutor Demo](YOUR_VIDEO_LINK_HERE)

The demo showcases the complete working flow of EduBridge AI Tutor, including student authentication, grade and subject selection, structured learning, AI-powered doubt solving, quizzes, assessments, progress tracking, and performance analysis.

---

# 📖 About EduBridge AI Tutor

EduBridge AI Tutor is a full-stack educational platform designed to provide school students with a personalized and interactive learning experience.

The platform brings structured learning content, AI-powered doubt solving, quizzes, assessments, progress tracking, and performance analysis together in one unified environment.

Instead of requiring students to use different platforms for studying concepts, clearing doubts, practicing questions, evaluating their understanding, and checking their progress, EduBridge integrates these activities into a single learning journey.

### 🎯 Learning Cycle

Learn → Ask → Practice → Assess → Analyze → Improve

The platform currently focuses on students from Grades 8–10 and provides a structured learning environment where students can select their grade, subject, and topic before beginning their learning activities.

---

# ✨ Core Features

## 🔐 1. Authentication & Personalized Student Experience

EduBridge provides a secure authentication system that allows students to create accounts and access their personalized learning environment.

The authentication system uses JWT-based authentication and securely hashed passwords. Protected backend endpoints ensure that student-specific information can only be accessed by authenticated users.

Each student's learning activity, quiz attempts, assessment results, progress, and performance information are associated with their individual account.

### Includes

- Student Signup
- Student Login
- Secure Password Hashing
- JWT-based Authentication
- Protected API Endpoints
- Student-specific Learning Data
- Personalized Dashboard

---

## 📚 2. Structured Learning & Educational Modules

The Learning Module provides structured educational content that students can study topic by topic.

Learning material is organized through:

Grade → Subject → Unit → Module → Topic → Learning Content

Students first select their grade and then navigate through subjects, units, modules, and topics to find the content they want to study.

The modular approach allows students to focus on individual concepts and makes the platform easier to expand with additional grades, subjects, modules, and learning material.

---

## 🤖 3. AI Tutor & RAG-Based Doubt Solving

The AI Tutor is one of the core features of EduBridge. It allows students to ask questions about concepts they are currently learning and receive explanations directly within the platform.

Students can ask the AI Tutor for:

- Concept explanations
- Examples
- Simplified explanations
- Clarifications
- Summaries
- Follow-up questions

The AI Tutor is powered by a Retrieval-Augmented Generation (RAG) pipeline.

Instead of sending the student's question directly to a language model, the system first searches for relevant educational information and uses the retrieved content as context while generating the response.

### RAG Pipeline

Student Question → Query Processing → Content Retrieval → Vector Similarity Search → Context Construction → LLM Generation → AI Tutor Response

The RAG system uses embeddings and ChromaDB for semantic retrieval and the Groq API for language-model generation.

The student's educational context, such as grade and subject, can also be considered during retrieval to improve the relevance of the generated response.

This allows the AI Tutor to provide responses grounded in the educational content available within the platform.

---

## 💬 4. Context-Aware AI Conversations

EduBridge's AI Tutor supports conversational interactions rather than treating every question as a completely independent request.

Students can continue asking questions based on previous responses.

For example:

Student: What is a variable?

AI Tutor: A variable is a symbol used to represent an unknown value.

Student: Give me an example.

AI Tutor: For example, in x + 5 = 10, x is the variable.

Student: Explain it in simpler words.

AI Tutor: Think of a variable as a box that can hold a value.

The conversational system supports:

- New Questions
- Follow-up Questions
- Clarifications
- Example Requests
- Summary Requests
- Greetings

This allows students to interact naturally with the AI Tutor while learning.

---

## 📝 5. Quiz & Practice Module

The Quiz Module allows students to test their understanding after studying a topic.

Students can select a subject and topic and attempt questions related to the corresponding learning content.

### Quiz Flow

Select Subject → Select Topic → Start Quiz → Answer Questions → Submit Quiz → View Result

The system manages quiz questions, answer options, student responses, attempts, and scores.

Quiz-related information includes:

- Quiz Questions
- Question Options
- Student Answers
- Quiz Attempts
- Scores
- Question Attempts
- Attempt Information

The quiz system connects directly with the learning module, allowing students to move from learning a concept to immediately practicing it.

---

## 📊 6. Assessment & Evaluation Module

The Assessment Module provides a broader evaluation of the student's understanding.

While quizzes are useful for topic-level practice, assessments allow students to evaluate their knowledge across a larger set of questions related to a subject.

### Assessment Flow

Select Grade → Select Subject → Start Assessment → Answer Questions → Submit Assessment → View Result

The system records assessment attempts, answers, scores, and results.

Assessment data can then be used by the performance system to provide a broader view of the student's academic progress.

This creates a complete evaluation cycle:

Learn → Practice → Assess → Analyze

---

## 📈 7. Progress Tracking & Performance Analysis

EduBridge maintains information about student activity across the learning, quiz, and assessment modules.

The Progress Module tracks information such as:

- Learning progress
- Completed learning activities
- Quiz attempts
- Assessment attempts
- Question attempts
- Scores

The Performance Analysis Module brings together this information to help students understand their academic performance.

### Performance Flow

Learning Activity + Quiz Results + Assessment Results → Performance Analysis → Identify Progress → Identify Areas for Improvement

This allows students to understand how they are performing rather than simply viewing individual quiz or assessment scores.

The combination of progress tracking and performance analysis creates a feedback loop that encourages students to identify weaker areas and continue practicing them.

---

## 👤 8. Student Profile & Dashboard

The Profile Module provides students with a dedicated area for their personal and account-related information.

The profile is connected to the authenticated student's account, ensuring that their learning activity and performance information remains associated with the correct student.

The Dashboard acts as the central navigation point for the platform.

Students can access:

- 📚 Learning
- 🤖 AI Tutor
- 📝 Quizzes
- 📊 Assessments
- 📈 Progress & Performance
- 👤 Profile

Together, the dashboard and profile provide a personalized environment where students can manage and continue their learning journey.

---

# 🏗️ System Architecture

EduBridge follows a modular full-stack architecture consisting of a React frontend, FastAPI backend, PostgreSQL database, and separate RAG/AI components.

Student → React + Vite Frontend → REST APIs → FastAPI Backend → PostgreSQL Database

The backend also communicates with the RAG/AI service for AI-powered doubt solving and retrieval.

---

# 🔄 Complete Student Journey

Login / Signup → Dashboard → Select Grade → Select Subject → Select Module / Topic → Learn → Ask AI Tutor → Practice Quiz → Take Assessment → View Results → Analyze Performance → Track Progress

---

# 🗄️ Database

EduBridge uses PostgreSQL as its primary relational database.

The database stores both educational content and student-related information.

### Major Data Entities

- Users
- Grades
- Subjects
- Units
- Modules
- Learning Content
- Quizzes
- Questions
- Question Options
- Quiz Attempts
- Question Attempts
- Assessments
- Assessment Attempts
- Student Progress
- Performance Data
- AI Conversations
- AI Messages

SQLAlchemy is used as the ORM to interact with the PostgreSQL database from the FastAPI backend.

---

# 🛠️ Technology Stack

## Frontend

- React
- Vite
- React Router
- JavaScript
- CSS

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- Passlib
- bcrypt
- Uvicorn

## Database

- PostgreSQL

## AI & RAG

- Python
- FastAPI
- ChromaDB
- Embeddings
- Retrieval-Augmented Generation
- Groq API

---

# 📂 Project Structure

EduBridge-AI-Tutor/

├── Frontend-mem1/
│   ├── src/
│   ├── App.jsx
│   └── main.jsx
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── seed_data.py
│   └── tests/
│
├── Rag/
│   ├── embedding/
│   ├── ingestion/
│   ├── llm/
│   ├── retrieval/
│   ├── rag_pipeline/
│   ├── vectorstore/
│   ├── api.py
│   └── requirements.txt
│
├── database/
│   └── seed.sql
│
├── .env.example
├── .gitignore
└── README.md

---

# ⚙️ Local Setup

## Prerequisites

- Python 3
- Node.js
- PostgreSQL
- Git

### Backend

cd backend

python -m venv venv

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Configure the required environment variables:

DATABASE_URL=your-postgresql-url
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key

Start the backend:

uvicorn app.main:app --reload

Backend:

http://127.0.0.1:8000

### Frontend

Open another terminal:

cd Frontend-mem1

npm install

npm run dev

Frontend:

http://localhost:5173

### RAG Service

cd Rag

pip install -r requirements.txt

Configure the required AI environment variables and start the RAG service according to the project's RAG configuration.

---

# 🔑 Environment Variables

DATABASE_URL=postgresql+psycopg2://username:password@host:5432/database

SECRET_KEY=your-secret-key

GROQ_API_KEY=your-groq-api-key

VITE_API_URL=http://127.0.0.1:8000

VITE_RAG_API_URL=http://127.0.0.1:8001

⚠️ Never commit real API keys, database passwords, or secret keys to GitHub.

Use .env.example to document required variables without exposing sensitive credentials.

---

# 🚀 Deployment

EduBridge can be deployed as separate services:

React Frontend → Vercel

FastAPI Backend → Render

RAG Service → Render

PostgreSQL Database → Render PostgreSQL

Environment variables such as database URLs, secret keys, API keys, and frontend API URLs should be configured directly on the respective deployment platforms.

---

# 🔒 Security

EduBridge incorporates several security practices:

- Password hashing
- JWT-based authentication
- Protected API endpoints
- Environment-based secrets
- Database-backed authentication
- Separation of frontend and backend services

Sensitive credentials should never be stored directly in the source code or committed to GitHub.

---

# 🌱 Future Enhancements

- 📱 Mobile Application
- 🎯 Adaptive Learning Recommendations
- 🧠 Adaptive Quiz Difficulty
- 📊 Advanced Learning Analytics
- 🃏 Flashcard-Based Revision
- 🏆 Gamification and Achievement Badges
- 🔔 Learning Reminders
- 🗣️ Voice-Based AI Tutor
- 🌐 Multi-language Support
- 👨‍🏫 Teacher Dashboard
- 👪 Parent Dashboard

---

# 👥 Team

EduBridge AI Tutor was developed collaboratively with contributions across:

- Frontend Development
- Backend & API Development
- Database Design
- AI / RAG Implementation
- Authentication
- Learning & Assessment Modules
- UI/UX Design

---

# 🎯 Project Highlights

| Area | Implementation |
|---|---|
| 🎓 Education | Grade-based structured learning |
| 🤖 AI | Context-aware AI Tutor |
| 🧠 RAG | Educational content retrieval |
| 📚 Learning | Modular topic-based content |
| 📝 Practice | Topic-based quizzes |
| 📊 Evaluation | Subject-based assessments |
| 📈 Progress | Student learning tracking |
| 📉 Analytics | Performance analysis |
| 🔐 Security | JWT authentication & password hashing |
| 🗄️ Database | PostgreSQL |
| ⚡ Backend | FastAPI |
| 💻 Frontend | React + Vite |

---

# 🎓 EduBridge AI Tutor

> Learn. Ask. Practice. Assess. Improve.

🎬 [Watch the Complete Project Demo](YOUR_VIDEO_LINK_HERE)
