--
-- PostgreSQL database dump
--

\restrict Go0ABtFHSE4iORHCEBuEzzCmAoUQY8xqWd6wGRZn4uDFf303EI3yC7WOzC5W1a2

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

-- Started on 2026-08-20 19:24:24

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 252 (class 1259 OID 16722)
-- Name: ai_conversations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_conversations (
    id integer NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.ai_conversations OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 16721)
-- Name: ai_conversations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ai_conversations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ai_conversations_id_seq OWNER TO postgres;

--
-- TOC entry 5259 (class 0 OID 0)
-- Dependencies: 251
-- Name: ai_conversations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ai_conversations_id_seq OWNED BY public.ai_conversations.id;


--
-- TOC entry 254 (class 1259 OID 16737)
-- Name: ai_messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_messages (
    id integer NOT NULL,
    conversation_id integer NOT NULL,
    sender character varying(20) NOT NULL,
    message text NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.ai_messages OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 16736)
-- Name: ai_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ai_messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ai_messages_id_seq OWNER TO postgres;

--
-- TOC entry 5260 (class 0 OID 0)
-- Dependencies: 253
-- Name: ai_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ai_messages_id_seq OWNED BY public.ai_messages.id;


--
-- TOC entry 244 (class 1259 OID 16642)
-- Name: assessment_attempts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.assessment_attempts (
    id integer NOT NULL,
    user_id integer NOT NULL,
    assessment_id integer NOT NULL,
    score integer,
    total_questions integer NOT NULL,
    started_at timestamp without time zone,
    completed_at timestamp without time zone
);


ALTER TABLE public.assessment_attempts OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 16641)
-- Name: assessment_attempts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.assessment_attempts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.assessment_attempts_id_seq OWNER TO postgres;

--
-- TOC entry 5261 (class 0 OID 0)
-- Dependencies: 243
-- Name: assessment_attempts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.assessment_attempts_id_seq OWNED BY public.assessment_attempts.id;


--
-- TOC entry 248 (class 1259 OID 16684)
-- Name: flashcards; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.flashcards (
    id integer NOT NULL,
    module_id integer NOT NULL,
    question text NOT NULL,
    answer text NOT NULL,
    difficulty character varying(30)
);


ALTER TABLE public.flashcards OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 16683)
-- Name: flashcards_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.flashcards_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.flashcards_id_seq OWNER TO postgres;

--
-- TOC entry 5262 (class 0 OID 0)
-- Dependencies: 247
-- Name: flashcards_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.flashcards_id_seq OWNED BY public.flashcards.id;


--
-- TOC entry 220 (class 1259 OID 16417)
-- Name: grades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.grades (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.grades OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16416)
-- Name: grades_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.grades_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.grades_id_seq OWNER TO postgres;

--
-- TOC entry 5263 (class 0 OID 0)
-- Dependencies: 219
-- Name: grades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.grades_id_seq OWNED BY public.grades.id;


--
-- TOC entry 230 (class 1259 OID 16505)
-- Name: learning_contents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.learning_contents (
    id integer NOT NULL,
    module_id integer NOT NULL,
    title character varying(200) NOT NULL,
    content_type character varying(30) NOT NULL,
    content text,
    media_url text,
    order_number integer NOT NULL
);


ALTER TABLE public.learning_contents OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16504)
-- Name: learning_contents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.learning_contents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.learning_contents_id_seq OWNER TO postgres;

--
-- TOC entry 5264 (class 0 OID 0)
-- Dependencies: 229
-- Name: learning_contents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.learning_contents_id_seq OWNED BY public.learning_contents.id;


--
-- TOC entry 228 (class 1259 OID 16487)
-- Name: modules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.modules (
    id integer NOT NULL,
    unit_id integer NOT NULL,
    title character varying(150) NOT NULL,
    description character varying(500),
    order_number integer NOT NULL,
    difficulty character varying(30)
);


ALTER TABLE public.modules OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16486)
-- Name: modules_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.modules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.modules_id_seq OWNER TO postgres;

--
-- TOC entry 5265 (class 0 OID 0)
-- Dependencies: 227
-- Name: modules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.modules_id_seq OWNED BY public.modules.id;


--
-- TOC entry 258 (class 1259 OID 16780)
-- Name: performance_analysis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.performance_analysis (
    id integer NOT NULL,
    user_id integer NOT NULL,
    module_id integer NOT NULL,
    total_attempts integer NOT NULL,
    correct_answers integer NOT NULL,
    total_questions integer NOT NULL,
    accuracy double precision NOT NULL,
    weakness_level character varying(50) NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.performance_analysis OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 16779)
-- Name: performance_analysis_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.performance_analysis_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.performance_analysis_id_seq OWNER TO postgres;

--
-- TOC entry 5266 (class 0 OID 0)
-- Dependencies: 257
-- Name: performance_analysis_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.performance_analysis_id_seq OWNED BY public.performance_analysis.id;


--
-- TOC entry 240 (class 1259 OID 16598)
-- Name: question_attempts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.question_attempts (
    id integer NOT NULL,
    attempt_id integer NOT NULL,
    question_id integer NOT NULL,
    selected_option_id integer,
    is_correct boolean NOT NULL,
    time_taken integer
);


ALTER TABLE public.question_attempts OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 16597)
-- Name: question_attempts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.question_attempts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.question_attempts_id_seq OWNER TO postgres;

--
-- TOC entry 5267 (class 0 OID 0)
-- Dependencies: 239
-- Name: question_attempts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.question_attempts_id_seq OWNED BY public.question_attempts.id;


--
-- TOC entry 236 (class 1259 OID 16559)
-- Name: question_options; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.question_options (
    id integer NOT NULL,
    question_id integer NOT NULL,
    option_text text NOT NULL,
    is_correct boolean NOT NULL
);


ALTER TABLE public.question_options OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16558)
-- Name: question_options_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.question_options_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.question_options_id_seq OWNER TO postgres;

--
-- TOC entry 5268 (class 0 OID 0)
-- Dependencies: 235
-- Name: question_options_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.question_options_id_seq OWNED BY public.question_options.id;


--
-- TOC entry 234 (class 1259 OID 16541)
-- Name: questions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.questions (
    id integer NOT NULL,
    quiz_id integer NOT NULL,
    question_text text NOT NULL,
    question_type character varying(30) NOT NULL,
    difficulty character varying(30),
    explanation text,
    is_approved boolean DEFAULT true
);


ALTER TABLE public.questions OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16540)
-- Name: questions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.questions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.questions_id_seq OWNER TO postgres;

--
-- TOC entry 5269 (class 0 OID 0)
-- Dependencies: 233
-- Name: questions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.questions_id_seq OWNED BY public.questions.id;


--
-- TOC entry 238 (class 1259 OID 16577)
-- Name: quiz_attempts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quiz_attempts (
    id integer NOT NULL,
    user_id integer NOT NULL,
    quiz_id integer NOT NULL,
    score integer,
    total_questions integer NOT NULL,
    started_at timestamp without time zone,
    completed_at timestamp without time zone,
    time_taken_seconds integer DEFAULT 0
);


ALTER TABLE public.quiz_attempts OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16576)
-- Name: quiz_attempts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.quiz_attempts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.quiz_attempts_id_seq OWNER TO postgres;

--
-- TOC entry 5270 (class 0 OID 0)
-- Dependencies: 237
-- Name: quiz_attempts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.quiz_attempts_id_seq OWNED BY public.quiz_attempts.id;


--
-- TOC entry 232 (class 1259 OID 16524)
-- Name: quizzes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quizzes (
    id integer NOT NULL,
    module_id integer NOT NULL,
    title character varying(200) NOT NULL,
    description text,
    time_limit integer,
    quiz_type character varying(30),
    time_limit_minutes integer DEFAULT 10
);


ALTER TABLE public.quizzes OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16523)
-- Name: quizzes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.quizzes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.quizzes_id_seq OWNER TO postgres;

--
-- TOC entry 5271 (class 0 OID 0)
-- Dependencies: 231
-- Name: quizzes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.quizzes_id_seq OWNED BY public.quizzes.id;


--
-- TOC entry 250 (class 1259 OID 16702)
-- Name: student_flashcards; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student_flashcards (
    id integer NOT NULL,
    user_id integer NOT NULL,
    flashcard_id integer NOT NULL,
    status character varying(30),
    last_reviewed timestamp without time zone,
    next_review timestamp without time zone
);


ALTER TABLE public.student_flashcards OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 16701)
-- Name: student_flashcards_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.student_flashcards_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.student_flashcards_id_seq OWNER TO postgres;

--
-- TOC entry 5272 (class 0 OID 0)
-- Dependencies: 249
-- Name: student_flashcards_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.student_flashcards_id_seq OWNED BY public.student_flashcards.id;


--
-- TOC entry 246 (class 1259 OID 16663)
-- Name: student_progress; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student_progress (
    id integer NOT NULL,
    user_id integer NOT NULL,
    module_id integer NOT NULL,
    completion_percentage double precision NOT NULL,
    mastery_score double precision,
    last_accessed timestamp without time zone
);


ALTER TABLE public.student_progress OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 16662)
-- Name: student_progress_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.student_progress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.student_progress_id_seq OWNER TO postgres;

--
-- TOC entry 5273 (class 0 OID 0)
-- Dependencies: 245
-- Name: student_progress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.student_progress_id_seq OWNED BY public.student_progress.id;


--
-- TOC entry 224 (class 1259 OID 16452)
-- Name: subjects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subjects (
    id integer NOT NULL,
    grade_id integer NOT NULL,
    name character varying(100) NOT NULL,
    description character varying(500)
);


ALTER TABLE public.subjects OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16451)
-- Name: subjects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subjects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subjects_id_seq OWNER TO postgres;

--
-- TOC entry 5274 (class 0 OID 0)
-- Dependencies: 223
-- Name: subjects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subjects_id_seq OWNED BY public.subjects.id;


--
-- TOC entry 242 (class 1259 OID 16624)
-- Name: unit_assessments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.unit_assessments (
    id integer NOT NULL,
    unit_id integer NOT NULL,
    title character varying(200) NOT NULL,
    description text,
    time_limit integer
);


ALTER TABLE public.unit_assessments OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 16623)
-- Name: unit_assessments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.unit_assessments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.unit_assessments_id_seq OWNER TO postgres;

--
-- TOC entry 5275 (class 0 OID 0)
-- Dependencies: 241
-- Name: unit_assessments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.unit_assessments_id_seq OWNED BY public.unit_assessments.id;


--
-- TOC entry 226 (class 1259 OID 16469)
-- Name: units; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.units (
    id integer NOT NULL,
    subject_id integer NOT NULL,
    title character varying(150) NOT NULL,
    description character varying(500),
    order_number integer NOT NULL
);


ALTER TABLE public.units OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16468)
-- Name: units_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.units_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.units_id_seq OWNER TO postgres;

--
-- TOC entry 5276 (class 0 OID 0)
-- Dependencies: 225
-- Name: units_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.units_id_seq OWNED BY public.units.id;


--
-- TOC entry 256 (class 1259 OID 16756)
-- Name: user_learning_content_progress; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_learning_content_progress (
    id integer NOT NULL,
    user_id integer NOT NULL,
    learning_content_id integer NOT NULL,
    completed_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.user_learning_content_progress OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 16755)
-- Name: user_learning_content_progress_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_learning_content_progress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_learning_content_progress_id_seq OWNER TO postgres;

--
-- TOC entry 5277 (class 0 OID 0)
-- Dependencies: 255
-- Name: user_learning_content_progress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_learning_content_progress_id_seq OWNED BY public.user_learning_content_progress.id;


--
-- TOC entry 260 (class 1259 OID 16809)
-- Name: user_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_profiles (
    id integer NOT NULL,
    user_id integer NOT NULL,
    profile_image_url character varying(500),
    preferred_language character varying(50),
    learning_goal character varying(500),
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.user_profiles OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 16808)
-- Name: user_profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_profiles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_profiles_id_seq OWNER TO postgres;

--
-- TOC entry 5278 (class 0 OID 0)
-- Dependencies: 259
-- Name: user_profiles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_profiles_id_seq OWNED BY public.user_profiles.id;


--
-- TOC entry 222 (class 1259 OID 16428)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role character varying(20) NOT NULL,
    grade_id integer,
    created_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16427)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 5279 (class 0 OID 0)
-- Dependencies: 221
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4976 (class 2604 OID 16725)
-- Name: ai_conversations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_conversations ALTER COLUMN id SET DEFAULT nextval('public.ai_conversations_id_seq'::regclass);


--
-- TOC entry 4977 (class 2604 OID 16740)
-- Name: ai_messages id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_messages ALTER COLUMN id SET DEFAULT nextval('public.ai_messages_id_seq'::regclass);


--
-- TOC entry 4972 (class 2604 OID 16645)
-- Name: assessment_attempts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assessment_attempts ALTER COLUMN id SET DEFAULT nextval('public.assessment_attempts_id_seq'::regclass);


--
-- TOC entry 4974 (class 2604 OID 16687)
-- Name: flashcards id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.flashcards ALTER COLUMN id SET DEFAULT nextval('public.flashcards_id_seq'::regclass);


--
-- TOC entry 4956 (class 2604 OID 16420)
-- Name: grades id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades ALTER COLUMN id SET DEFAULT nextval('public.grades_id_seq'::regclass);


--
-- TOC entry 4962 (class 2604 OID 16508)
-- Name: learning_contents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.learning_contents ALTER COLUMN id SET DEFAULT nextval('public.learning_contents_id_seq'::regclass);


--
-- TOC entry 4961 (class 2604 OID 16490)
-- Name: modules id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modules ALTER COLUMN id SET DEFAULT nextval('public.modules_id_seq'::regclass);


--
-- TOC entry 4980 (class 2604 OID 16783)
-- Name: performance_analysis id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.performance_analysis ALTER COLUMN id SET DEFAULT nextval('public.performance_analysis_id_seq'::regclass);


--
-- TOC entry 4970 (class 2604 OID 16601)
-- Name: question_attempts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_attempts ALTER COLUMN id SET DEFAULT nextval('public.question_attempts_id_seq'::regclass);


--
-- TOC entry 4967 (class 2604 OID 16562)
-- Name: question_options id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_options ALTER COLUMN id SET DEFAULT nextval('public.question_options_id_seq'::regclass);


--
-- TOC entry 4965 (class 2604 OID 16544)
-- Name: questions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions ALTER COLUMN id SET DEFAULT nextval('public.questions_id_seq'::regclass);


--
-- TOC entry 4968 (class 2604 OID 16580)
-- Name: quiz_attempts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quiz_attempts ALTER COLUMN id SET DEFAULT nextval('public.quiz_attempts_id_seq'::regclass);


--
-- TOC entry 4963 (class 2604 OID 16527)
-- Name: quizzes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quizzes ALTER COLUMN id SET DEFAULT nextval('public.quizzes_id_seq'::regclass);


--
-- TOC entry 4975 (class 2604 OID 16705)
-- Name: student_flashcards id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_flashcards ALTER COLUMN id SET DEFAULT nextval('public.student_flashcards_id_seq'::regclass);


--
-- TOC entry 4973 (class 2604 OID 16666)
-- Name: student_progress id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_progress ALTER COLUMN id SET DEFAULT nextval('public.student_progress_id_seq'::regclass);


--
-- TOC entry 4959 (class 2604 OID 16455)
-- Name: subjects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects ALTER COLUMN id SET DEFAULT nextval('public.subjects_id_seq'::regclass);


--
-- TOC entry 4971 (class 2604 OID 16627)
-- Name: unit_assessments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.unit_assessments ALTER COLUMN id SET DEFAULT nextval('public.unit_assessments_id_seq'::regclass);


--
-- TOC entry 4960 (class 2604 OID 16472)
-- Name: units id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.units ALTER COLUMN id SET DEFAULT nextval('public.units_id_seq'::regclass);


--
-- TOC entry 4978 (class 2604 OID 16759)
-- Name: user_learning_content_progress id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_learning_content_progress ALTER COLUMN id SET DEFAULT nextval('public.user_learning_content_progress_id_seq'::regclass);


--
-- TOC entry 4982 (class 2604 OID 16812)
-- Name: user_profiles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_profiles ALTER COLUMN id SET DEFAULT nextval('public.user_profiles_id_seq'::regclass);


--
-- TOC entry 4957 (class 2604 OID 16431)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 5245 (class 0 OID 16722)
-- Dependencies: 252
-- Data for Name: ai_conversations; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5237 (class 0 OID 16642)
-- Dependencies: 244
-- Data for Name: assessment_attempts; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5213 (class 0 OID 16417)
-- Dependencies: 220
-- Data for Name: grades; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.grades (id, name) FROM stdin;
1	Grade 8
2	Grade 9
3	Grade 10
\.


--
-- TOC entry 5223 (class 0 OID 16505)
-- Dependencies: 230
-- Data for Name: learning_contents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.learning_contents (id, module_id, title, content_type, content, media_url, order_number) FROM stdin;
1	1	Algebra	text	Algebra is a branch of mathematics that uses letters and symbols to represent unknown values.\n\nExamples:\n- x + 5 = 10, so x = 5.\n- 2x = 10, so x = 5.\n\nKey points:\n- Variables represent unknown values.\n- Expressions can contain numbers, variables, and operators.\n- Equations contain an equality sign.	\N	1
3	10	Geometry	text	Geometry is a branch of mathematics that deals with shapes, sizes, angles, and spatial relationships.\r\n\r\nExamples:\r\n- A triangle has 3 sides.\r\n- A rectangle has 4 sides and 4 right angles.\r\n- A square has 4 equal sides.\r\n\r\nKey points:\r\n- Shapes have different properties.\r\n- Angles measure turns between lines.\r\n- Perimeter is the distance around a shape.\r\n- Area measures the space inside a shape.	\N	1
4	11	Fractions	text	A fraction represents a part of a whole using a numerator and a denominator.\r\n\r\nExamples:\r\n- 1/2 represents one out of two equal parts.\r\n- 3/4 represents three out of four equal parts.\r\n- 2/5 represents two out of five equal parts.\r\n\r\nKey points:\r\n- The numerator is the top number.\r\n- The denominator is the bottom number.\r\n- Fractions can represent parts of a whole.\r\n- Equivalent fractions have the same value.	\N	1
5	2	Physics	text	Physics is the branch of science that studies matter, energy, motion, forces, and how objects interact.\r\n\r\nExamples:\r\n- A moving car has motion.\r\n- A force can push or pull an object.\r\n- Gravity pulls objects toward Earth.\r\n\r\nKey points:\r\n- Motion describes how an object changes position.\r\n- Force is a push or pull.\r\n- Energy allows objects to do work.\r\n- Gravity attracts objects toward Earth.	\N	1
6	5	Physics	text	Physics is the branch of science that studies matter, energy, motion, forces, and how objects interact.\r\n\r\nExamples:\r\n- A moving car has motion.\r\n- A force can push or pull an object.\r\n- Gravity pulls objects toward Earth.\r\n\r\nKey points:\r\n- Motion describes how an object changes position.\r\n- Force is a push or pull.\r\n- Energy allows objects to do work.\r\n- Gravity attracts objects toward Earth.	\N	1
7	8	Physics	text	Physics is the branch of science that studies matter, energy, motion, forces, and how objects interact.\r\n\r\nExamples:\r\n- A moving car has motion.\r\n- A force can push or pull an object.\r\n- Gravity pulls objects toward Earth.\r\n\r\nKey points:\r\n- Motion describes how an object changes position.\r\n- Force is a push or pull.\r\n- Energy allows objects to do work.\r\n- Gravity attracts objects toward Earth.	\N	1
8	12	Chemistry	text	Chemistry is the branch of science that studies matter, its properties, and the changes it undergoes.\r\n\r\nExamples:\r\n- Water is made of hydrogen and oxygen.\r\n- Melting ice is a physical change.\r\n- Rusting iron is a chemical change.\r\n\r\nKey points:\r\n- Matter has mass and occupies space.\r\n- Elements are made of one type of atom.\r\n- Compounds contain two or more elements.\r\n- Chemical reactions form new substances.	\N	1
9	18	Chemistry	text	Chemistry is the branch of science that studies matter, its properties, and the changes it undergoes.\r\n\r\nExamples:\r\n- Water is made of hydrogen and oxygen.\r\n- Melting ice is a physical change.\r\n- Rusting iron is a chemical change.\r\n\r\nKey points:\r\n- Matter has mass and occupies space.\r\n- Elements are made of one type of atom.\r\n- Compounds contain two or more elements.\r\n- Chemical reactions form new substances.	\N	1
10	24	Chemistry	text	Chemistry is the branch of science that studies matter, its properties, and the changes it undergoes.\r\n\r\nExamples:\r\n- Water is made of hydrogen and oxygen.\r\n- Melting ice is a physical change.\r\n- Rusting iron is a chemical change.\r\n\r\nKey points:\r\n- Matter has mass and occupies space.\r\n- Elements are made of one type of atom.\r\n- Compounds contain two or more elements.\r\n- Chemical reactions form new substances.	\N	1
11	13	Biology	text	Biology is the branch of science that studies living organisms and their life processes.\r\n\r\nExamples:\r\n- Plants make food through photosynthesis.\r\n- Humans breathe using their respiratory system.\r\n- Cells are the basic units of living organisms.\r\n\r\nKey points:\r\n- All living organisms are made of cells.\r\n- Plants and animals have different characteristics.\r\n- Living organisms grow and reproduce.\r\n- Organisms interact with their environment.	\N	1
12	19	Biology	text	Biology is the branch of science that studies living organisms and their life processes.\r\n\r\nExamples:\r\n- Plants make food through photosynthesis.\r\n- Humans breathe using their respiratory system.\r\n- Cells are the basic units of living organisms.\r\n\r\nKey points:\r\n- All living organisms are made of cells.\r\n- Plants and animals have different characteristics.\r\n- Living organisms grow and reproduce.\r\n- Organisms interact with their environment.	\N	1
13	25	Biology	text	Biology is the branch of science that studies living organisms and their life processes.\r\n\r\nExamples:\r\n- Plants make food through photosynthesis.\r\n- Humans breathe using their respiratory system.\r\n- Cells are the basic units of living organisms.\r\n\r\nKey points:\r\n- All living organisms are made of cells.\r\n- Plants and animals have different characteristics.\r\n- Living organisms grow and reproduce.\r\n- Organisms interact with their environment.	\N	1
14	3	Grammar	text	Grammar is the set of rules that helps us use words and sentences correctly.\r\n\r\nExamples:\r\n- She goes to school every day.\r\n- They are playing football.\r\n- I have finished my homework.\r\n\r\nKey points:\r\n- A sentence should have a clear structure.\r\n- Verbs show actions or states.\r\n- Tenses tell us when an action happens.\r\n- Punctuation helps make sentences clear.	\N	1
15	6	Grammar	text	Grammar is the set of rules that helps us use words and sentences correctly.\r\n\r\nExamples:\r\n- She goes to school every day.\r\n- They are playing football.\r\n- I have finished my homework.\r\n\r\nKey points:\r\n- A sentence should have a clear structure.\r\n- Verbs show actions or states.\r\n- Tenses tell us when an action happens.\r\n- Punctuation helps make sentences clear.	\N	1
16	9	Grammar	text	Grammar is the set of rules that helps us use words and sentences correctly.\r\n\r\nExamples:\r\n- She goes to school every day.\r\n- They are playing football.\r\n- I have finished my homework.\r\n\r\nKey points:\r\n- A sentence should have a clear structure.\r\n- Verbs show actions or states.\r\n- Tenses tell us when an action happens.\r\n- Punctuation helps make sentences clear.	\N	1
17	14	Vocabulary	text	Vocabulary is the collection of words that a person knows and uses.\r\n\r\nExamples:\r\n- Happy means feeling pleasure or joy.\r\n- Rapid means happening very quickly.\r\n- Ancient means belonging to a very old time.\r\n\r\nKey points:\r\n- Learning new words improves communication.\r\n- Synonyms are words with similar meanings.\r\n- Antonyms are words with opposite meanings.\r\n- Context helps us understand the meaning of a word.	\N	1
18	20	Vocabulary	text	Vocabulary is the collection of words that a person knows and uses.\r\n\r\nExamples:\r\n- Happy means feeling pleasure or joy.\r\n- Rapid means happening very quickly.\r\n- Ancient means belonging to a very old time.\r\n\r\nKey points:\r\n- Learning new words improves communication.\r\n- Synonyms are words with similar meanings.\r\n- Antonyms are words with opposite meanings.\r\n- Context helps us understand the meaning of a word.	\N	1
19	26	Vocabulary	text	Vocabulary is the collection of words that a person knows and uses.\r\n\r\nExamples:\r\n- Happy means feeling pleasure or joy.\r\n- Rapid means happening very quickly.\r\n- Ancient means belonging to a very old time.\r\n\r\nKey points:\r\n- Learning new words improves communication.\r\n- Synonyms are words with similar meanings.\r\n- Antonyms are words with opposite meanings.\r\n- Context helps us understand the meaning of a word.	\N	1
20	15	Reading	text	Reading is the process of understanding and interpreting written information.\r\n\r\nExamples:\r\n- Reading a story helps us understand characters and events.\r\n- Reading an article helps us identify important information.\r\n- Reading a poem helps us understand ideas and emotions.\r\n\r\nKey points:\r\n- Identify the main idea of a passage.\r\n- Look for important supporting details.\r\n- Use context to understand unfamiliar words.\r\n- Summarize what you have read.	\N	1
21	21	Reading	text	Reading is the process of understanding and interpreting written information.\r\n\r\nExamples:\r\n- Reading a story helps us understand characters and events.\r\n- Reading an article helps us identify important information.\r\n- Reading a poem helps us understand ideas and emotions.\r\n\r\nKey points:\r\n- Identify the main idea of a passage.\r\n- Look for important supporting details.\r\n- Use context to understand unfamiliar words.\r\n- Summarize what you have read.	\N	1
22	27	Reading	text	Reading is the process of understanding and interpreting written information.\r\n\r\nExamples:\r\n- Reading a story helps us understand characters and events.\r\n- Reading an article helps us identify important information.\r\n- Reading a poem helps us understand ideas and emotions.\r\n\r\nKey points:\r\n- Identify the main idea of a passage.\r\n- Look for important supporting details.\r\n- Use context to understand unfamiliar words.\r\n- Summarize what you have read.	\N	1
\.


--
-- TOC entry 5221 (class 0 OID 16487)
-- Dependencies: 228
-- Data for Name: modules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.modules (id, unit_id, title, description, order_number, difficulty) FROM stdin;
1	1	Algebra	Algebra learning module	1	Medium
10	1	Geometry	Geometry learning module	2	Medium
11	1	Fractions	Fractions learning module	3	Medium
2	2	Physics	Physics learning module	1	Medium
12	2	Chemistry	Chemistry learning module	2	Medium
13	2	Biology	Biology learning module	3	Medium
3	3	Grammar	Grammar learning module	1	Medium
14	3	Vocabulary	Vocabulary learning module	2	Medium
15	3	Reading	Reading learning module	3	Medium
4	4	Algebra	Algebra learning module	1	Medium
16	4	Geometry	Geometry learning module	2	Medium
17	4	Fractions	Fractions learning module	3	Medium
5	5	Physics	Physics learning module	1	Medium
18	5	Chemistry	Chemistry learning module	2	Medium
19	5	Biology	Biology learning module	3	Medium
6	6	Grammar	Grammar learning module	1	Medium
20	6	Vocabulary	Vocabulary learning module	2	Medium
21	6	Reading	Reading learning module	3	Medium
7	7	Algebra	Algebra learning module	1	Medium
22	7	Geometry	Geometry learning module	2	Medium
23	7	Fractions	Fractions learning module	3	Medium
8	8	Physics	Physics learning module	1	Medium
24	8	Chemistry	Chemistry learning module	2	Medium
25	8	Biology	Biology learning module	3	Medium
9	9	Grammar	Grammar learning module	1	Medium
26	9	Vocabulary	Vocabulary learning module	2	Medium
27	9	Reading	Reading learning module	3	Medium
\.


--
-- TOC entry 5251 (class 0 OID 16780)
-- Dependencies: 258
-- Data for Name: performance_analysis; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5231 (class 0 OID 16577)
-- Dependencies: 238
-- Data for Name: quiz_attempts; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5243 (class 0 OID 16702)
-- Dependencies: 250
-- Data for Name: student_flashcards; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5235 (class 0 OID 16624)
-- Dependencies: 242
-- Data for Name: unit_assessments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.unit_assessments (id, unit_id, title, description, time_limit) FROM stdin;
\.


--
-- TOC entry 5219 (class 0 OID 16469)
-- Dependencies: 226
-- Data for Name: units; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.units (id, subject_id, title, description, order_number) FROM stdin;
1	1	Introduction to Mathematics	Core introductory unit	1
2	2	Introduction to Science	Core introductory unit	1
3	3	Introduction to English	Core introductory unit	1
4	4	Introduction to Mathematics	Core introductory unit	1
5	5	Introduction to Science	Core introductory unit	1
6	6	Introduction to English	Core introductory unit	1
7	7	Introduction to Mathematics	Core introductory unit	1
8	8	Introduction to Science	Core introductory unit	1
9	9	Introduction to English	Core introductory unit	1
\.


--
-- TOC entry 5249 (class 0 OID 16756)
-- Dependencies: 256
-- Data for Name: user_learning_content_progress; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_learning_content_progress (id, user_id, learning_content_id, completed_at) FROM stdin;
1	1	1	2026-08-20 07:57:32.854866
2	4	1	2026-08-20 18:12:10.159732
3	1	17	2026-08-20 19:15:28.415091
\.


--
-- TOC entry 5253 (class 0 OID 16809)
-- Dependencies: 260
-- Data for Name: user_profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5215 (class 0 OID 16428)
-- Dependencies: 222
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5280 (class 0 OID 0)
-- Dependencies: 251
-- Name: ai_conversations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ai_conversations_id_seq', 1, false);


--
-- TOC entry 5281 (class 0 OID 0)
-- Dependencies: 253
-- Name: ai_messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ai_messages_id_seq', 1, false);


--
-- TOC entry 5282 (class 0 OID 0)
-- Dependencies: 243
-- Name: assessment_attempts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.assessment_attempts_id_seq', 1, false);


--
-- TOC entry 5283 (class 0 OID 0)
-- Dependencies: 247
-- Name: flashcards_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.flashcards_id_seq', 1, false);


--
-- TOC entry 5284 (class 0 OID 0)
-- Dependencies: 219
-- Name: grades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.grades_id_seq', 3, true);


--
-- TOC entry 5285 (class 0 OID 0)
-- Dependencies: 229
-- Name: learning_contents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.learning_contents_id_seq', 22, true);


--
-- TOC entry 5286 (class 0 OID 0)
-- Dependencies: 227
-- Name: modules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.modules_id_seq', 27, true);


--
-- TOC entry 5287 (class 0 OID 0)
-- Dependencies: 257
-- Name: performance_analysis_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.performance_analysis_id_seq', 1, false);


--
-- TOC entry 5288 (class 0 OID 0)
-- Dependencies: 239
-- Name: question_attempts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.question_attempts_id_seq', 1, false);


--
-- TOC entry 5289 (class 0 OID 0)
-- Dependencies: 235
-- Name: question_options_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.question_options_id_seq', 1, false);


--
-- TOC entry 5290 (class 0 OID 0)
-- Dependencies: 233
-- Name: questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.questions_id_seq', 1, false);


--
-- TOC entry 5291 (class 0 OID 0)
-- Dependencies: 237
-- Name: quiz_attempts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.quiz_attempts_id_seq', 1, false);


--
-- TOC entry 5292 (class 0 OID 0)
-- Dependencies: 231
-- Name: quizzes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.quizzes_id_seq', 1, false);


--
-- TOC entry 5293 (class 0 OID 0)
-- Dependencies: 249
-- Name: student_flashcards_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.student_flashcards_id_seq', 1, false);


--
-- TOC entry 5294 (class 0 OID 0)
-- Dependencies: 245
-- Name: student_progress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.student_progress_id_seq', 3, true);


--
-- TOC entry 5295 (class 0 OID 0)
-- Dependencies: 223
-- Name: subjects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subjects_id_seq', 9, true);


--
-- TOC entry 5296 (class 0 OID 0)
-- Dependencies: 241
-- Name: unit_assessments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.unit_assessments_id_seq', 1, false);


--
-- TOC entry 5297 (class 0 OID 0)
-- Dependencies: 225
-- Name: units_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.units_id_seq', 9, true);


--
-- TOC entry 5298 (class 0 OID 0)
-- Dependencies: 255
-- Name: user_learning_content_progress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_learning_content_progress_id_seq', 3, true);


--
-- TOC entry 5299 (class 0 OID 0)
-- Dependencies: 259
-- Name: user_profiles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_profiles_id_seq', 3, true);


--
-- TOC entry 5300 (class 0 OID 0)
-- Dependencies: 221
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- TOC entry 5022 (class 2606 OID 16730)
-- Name: ai_conversations ai_conversations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_conversations
    ADD CONSTRAINT ai_conversations_pkey PRIMARY KEY (id);


--
-- TOC entry 5024 (class 2606 OID 16749)
-- Name: ai_messages ai_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_messages
    ADD CONSTRAINT ai_messages_pkey PRIMARY KEY (id);


--
-- TOC entry 5014 (class 2606 OID 16651)
-- Name: assessment_attempts assessment_attempts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assessment_attempts
    ADD CONSTRAINT assessment_attempts_pkey PRIMARY KEY (id);


--
-- TOC entry 5018 (class 2606 OID 16695)
-- Name: flashcards flashcards_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.flashcards
    ADD CONSTRAINT flashcards_pkey PRIMARY KEY (id);


--
-- TOC entry 4986 (class 2606 OID 16426)
-- Name: grades grades_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades
    ADD CONSTRAINT grades_name_key UNIQUE (name);


--
-- TOC entry 4988 (class 2606 OID 16424)
-- Name: grades grades_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades
    ADD CONSTRAINT grades_pkey PRIMARY KEY (id);


--
-- TOC entry 5000 (class 2606 OID 16517)
-- Name: learning_contents learning_contents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.learning_contents
    ADD CONSTRAINT learning_contents_pkey PRIMARY KEY (id);


--
-- TOC entry 4998 (class 2606 OID 16498)
-- Name: modules modules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modules
    ADD CONSTRAINT modules_pkey PRIMARY KEY (id);


--
-- TOC entry 5030 (class 2606 OID 16795)
-- Name: performance_analysis performance_analysis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.performance_analysis
    ADD CONSTRAINT performance_analysis_pkey PRIMARY KEY (id);


--
-- TOC entry 5010 (class 2606 OID 16607)
-- Name: question_attempts question_attempts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_attempts
    ADD CONSTRAINT question_attempts_pkey PRIMARY KEY (id);


--
-- TOC entry 5006 (class 2606 OID 16570)
-- Name: question_options question_options_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_options
    ADD CONSTRAINT question_options_pkey PRIMARY KEY (id);


--
-- TOC entry 5004 (class 2606 OID 16552)
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);


--
-- TOC entry 5008 (class 2606 OID 16586)
-- Name: quiz_attempts quiz_attempts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quiz_attempts
    ADD CONSTRAINT quiz_attempts_pkey PRIMARY KEY (id);


--
-- TOC entry 5002 (class 2606 OID 16534)
-- Name: quizzes quizzes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quizzes
    ADD CONSTRAINT quizzes_pkey PRIMARY KEY (id);


--
-- TOC entry 5020 (class 2606 OID 16710)
-- Name: student_flashcards student_flashcards_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_flashcards
    ADD CONSTRAINT student_flashcards_pkey PRIMARY KEY (id);


--
-- TOC entry 5016 (class 2606 OID 16672)
-- Name: student_progress student_progress_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_progress
    ADD CONSTRAINT student_progress_pkey PRIMARY KEY (id);


--
-- TOC entry 4994 (class 2606 OID 16462)
-- Name: subjects subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_pkey PRIMARY KEY (id);


--
-- TOC entry 5012 (class 2606 OID 16634)
-- Name: unit_assessments unit_assessments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.unit_assessments
    ADD CONSTRAINT unit_assessments_pkey PRIMARY KEY (id);


--
-- TOC entry 4996 (class 2606 OID 16480)
-- Name: units units_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.units
    ADD CONSTRAINT units_pkey PRIMARY KEY (id);


--
-- TOC entry 5026 (class 2606 OID 16768)
-- Name: user_learning_content_progress uq_user_learning_content_progress; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_learning_content_progress
    ADD CONSTRAINT uq_user_learning_content_progress UNIQUE (user_id, learning_content_id);


--
-- TOC entry 5032 (class 2606 OID 16797)
-- Name: performance_analysis uq_user_module_performance; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.performance_analysis
    ADD CONSTRAINT uq_user_module_performance UNIQUE (user_id, module_id);


--
-- TOC entry 5028 (class 2606 OID 16766)
-- Name: user_learning_content_progress user_learning_content_progress_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_learning_content_progress
    ADD CONSTRAINT user_learning_content_progress_pkey PRIMARY KEY (id);


--
-- TOC entry 5034 (class 2606 OID 16822)
-- Name: user_profiles user_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_pkey PRIMARY KEY (id);


--
-- TOC entry 5036 (class 2606 OID 16824)
-- Name: user_profiles user_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_user_id_key UNIQUE (user_id);


--
-- TOC entry 4992 (class 2606 OID 16443)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4989 (class 1259 OID 16449)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 4990 (class 1259 OID 16450)
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- TOC entry 5058 (class 2606 OID 16731)
-- Name: ai_conversations ai_conversations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_conversations
    ADD CONSTRAINT ai_conversations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 5059 (class 2606 OID 16750)
-- Name: ai_messages ai_messages_conversation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_messages
    ADD CONSTRAINT ai_messages_conversation_id_fkey FOREIGN KEY (conversation_id) REFERENCES public.ai_conversations(id);


--
-- TOC entry 5051 (class 2606 OID 16657)
-- Name: assessment_attempts assessment_attempts_assessment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assessment_attempts
    ADD CONSTRAINT assessment_attempts_assessment_id_fkey FOREIGN KEY (assessment_id) REFERENCES public.unit_assessments(id);


--
-- TOC entry 5052 (class 2606 OID 16652)
-- Name: assessment_attempts assessment_attempts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assessment_attempts
    ADD CONSTRAINT assessment_attempts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 5055 (class 2606 OID 16696)
-- Name: flashcards flashcards_module_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.flashcards
    ADD CONSTRAINT flashcards_module_id_fkey FOREIGN KEY (module_id) REFERENCES public.modules(id);


--
-- TOC entry 5041 (class 2606 OID 16518)
-- Name: learning_contents learning_contents_module_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.learning_contents
    ADD CONSTRAINT learning_contents_module_id_fkey FOREIGN KEY (module_id) REFERENCES public.modules(id);


--
-- TOC entry 5040 (class 2606 OID 16499)
-- Name: modules modules_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modules
    ADD CONSTRAINT modules_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.units(id);


--
-- TOC entry 5062 (class 2606 OID 16803)
-- Name: performance_analysis performance_analysis_module_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.performance_analysis
    ADD CONSTRAINT performance_analysis_module_id_fkey FOREIGN KEY (module_id) REFERENCES public.modules(id);


--
-- TOC entry 5063 (class 2606 OID 16798)
-- Name: performance_analysis performance_analysis_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.performance_analysis
    ADD CONSTRAINT performance_analysis_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 5047 (class 2606 OID 16608)
-- Name: question_attempts question_attempts_attempt_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_attempts
    ADD CONSTRAINT question_attempts_attempt_id_fkey FOREIGN KEY (attempt_id) REFERENCES public.quiz_attempts(id);


--
-- TOC entry 5048 (class 2606 OID 16613)
-- Name: question_attempts question_attempts_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_attempts
    ADD CONSTRAINT question_attempts_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id);


--
-- TOC entry 5049 (class 2606 OID 16618)
-- Name: question_attempts question_attempts_selected_option_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_attempts
    ADD CONSTRAINT question_attempts_selected_option_id_fkey FOREIGN KEY (selected_option_id) REFERENCES public.question_options(id);


--
-- TOC entry 5044 (class 2606 OID 16571)
-- Name: question_options question_options_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_options
    ADD CONSTRAINT question_options_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id);


--
-- TOC entry 5043 (class 2606 OID 16553)
-- Name: questions questions_quiz_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_quiz_id_fkey FOREIGN KEY (quiz_id) REFERENCES public.quizzes(id);


--
-- TOC entry 5045 (class 2606 OID 16592)
-- Name: quiz_attempts quiz_attempts_quiz_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quiz_attempts
    ADD CONSTRAINT quiz_attempts_quiz_id_fkey FOREIGN KEY (quiz_id) REFERENCES public.quizzes(id);


--
-- TOC entry 5046 (class 2606 OID 16587)
-- Name: quiz_attempts quiz_attempts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quiz_attempts
    ADD CONSTRAINT quiz_attempts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 5042 (class 2606 OID 16535)
-- Name: quizzes quizzes_module_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quizzes
    ADD CONSTRAINT quizzes_module_id_fkey FOREIGN KEY (module_id) REFERENCES public.modules(id);


--
-- TOC entry 5056 (class 2606 OID 16716)
-- Name: student_flashcards student_flashcards_flashcard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_flashcards
    ADD CONSTRAINT student_flashcards_flashcard_id_fkey FOREIGN KEY (flashcard_id) REFERENCES public.flashcards(id);


--
-- TOC entry 5057 (class 2606 OID 16711)
-- Name: student_flashcards student_flashcards_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_flashcards
    ADD CONSTRAINT student_flashcards_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 5053 (class 2606 OID 16678)
-- Name: student_progress student_progress_module_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_progress
    ADD CONSTRAINT student_progress_module_id_fkey FOREIGN KEY (module_id) REFERENCES public.modules(id);


--
-- TOC entry 5054 (class 2606 OID 16673)
-- Name: student_progress student_progress_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_progress
    ADD CONSTRAINT student_progress_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 5038 (class 2606 OID 16463)
-- Name: subjects subjects_grade_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_grade_id_fkey FOREIGN KEY (grade_id) REFERENCES public.grades(id);


--
-- TOC entry 5050 (class 2606 OID 16635)
-- Name: unit_assessments unit_assessments_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.unit_assessments
    ADD CONSTRAINT unit_assessments_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.units(id);


--
-- TOC entry 5039 (class 2606 OID 16481)
-- Name: units units_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.units
    ADD CONSTRAINT units_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.subjects(id);


--
-- TOC entry 5060 (class 2606 OID 16774)
-- Name: user_learning_content_progress user_learning_content_progress_learning_content_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_learning_content_progress
    ADD CONSTRAINT user_learning_content_progress_learning_content_id_fkey FOREIGN KEY (learning_content_id) REFERENCES public.learning_contents(id);


--
-- TOC entry 5061 (class 2606 OID 16769)
-- Name: user_learning_content_progress user_learning_content_progress_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_learning_content_progress
    ADD CONSTRAINT user_learning_content_progress_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 5064 (class 2606 OID 16825)
-- Name: user_profiles user_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 5037 (class 2606 OID 16444)
-- Name: users users_grade_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_grade_id_fkey FOREIGN KEY (grade_id) REFERENCES public.grades(id);


-- Completed on 2026-08-20 19:24:25

--
-- PostgreSQL database dump complete
--

\unrestrict Go0ABtFHSE4iORHCEBuEzzCmAoUQY8xqWd6wGRZn4uDFf303EI3yC7WOzC5W1a2


