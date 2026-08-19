"""
AI Assessment Service for generating Unit Assessment theoretical practice/reference questions.
Generates exactly 10 Short Answer Questions (SAQ) and 10 Long Answer Questions (LAQ).
NO model answers, NO scoring, NO grading.
"""

def generate_unit_assessment_questions(unit_title: str, subject_name: str = "", unit_description: str = "") -> dict[str, list[str]]:
    topic = unit_title.strip() or "Core Subject Concepts"
    subj = subject_name.strip() or "Curriculum"
    desc = unit_description.strip() if unit_description else f"Foundational and advanced principles of {topic}"

    # Exactly 10 Short Answer Questions (SAQ)
    saq_questions = [
        f"Define the fundamental concept of {topic} in {subj}.",
        f"State the primary theorem or core rule governing {topic}.",
        f"What are the key terms and standard notation associated with {topic}?",
        f"Give two real-world examples or applications of {topic}.",
        f"Explain the difference between direct and indirect properties in {topic}.",
        f"Identify the essential assumptions required when analyzing {topic}.",
        f"What is the standard formula or principle used to solve basic problems in {topic}?",
        f"Briefly describe how {topic} relates to other topics in {subj}.",
        f"What are common mistakes or misconceptions encountered when studying {topic}?",
        f"Summarize the key outcome or objective of studying {topic} in 2-3 sentences."
    ]

    # Exactly 10 Long Answer Questions (LAQ)
    laq_questions = [
        f"Provide a comprehensive overview of {topic}, explaining its theoretical foundation, historical context, and practical importance.",
        f"Derive or explain in detail the main mathematical, logical, or scientific principles underpinning {topic}.",
        f"Analyze a complex scenario involving {topic}. Break down the step-by-step methodology required to reach a complete solution.",
        f"Critically compare and contrast the different approaches or methods used to evaluate and solve problems in {topic}.",
        f"Discuss the practical engineering, scientific, or socioeconomic implications of {topic} in modern industry.",
        f"Describe how varying parameters or environmental conditions impact the behavior and outcomes within {topic}.",
        f"Develop a structured problem-solving framework that students can apply to master advanced problems in {topic}.",
        f"Evaluate the strengths and limitations of standard models used in {topic} and propose potential extensions.",
        f"Explain in depth how {topic} integrates with higher-level concepts across multidisciplinary domains in {subj}.",
        f"Construct a comprehensive case study illustrating how principles of {topic} are applied to solve large-scale real-world challenges."
    ]

    return {
        "short_answer_questions": saq_questions[:10],
        "long_answer_questions": laq_questions[:10]
    }


def generate_single_mcq_question(
    module_title: str,
    difficulty: str = "Medium",
    module_description: str = "",
    order_number: int = 1
) -> dict:
    """
    Generates a single MCQ with exactly 4 options, difficulty, 4 marks, and 1 correct option.
    """
    topic = module_title.strip() or "Core Module Concept"
    diff = difficulty.capitalize() if difficulty in ["Easy", "Medium", "Hard"] else "Medium"

    if diff == "Easy":
        q_text = f"What is the basic definition or core rule of {topic}?"
        opts = [
            {"option_text": f"The standard foundational principle governing {topic}", "is_correct": True, "order_number": 1},
            {"option_text": f"An unrelated formula used exclusively outside of {topic}", "is_correct": False, "order_number": 2},
            {"option_text": f"A deprecated rule that does not apply to {topic}", "is_correct": False, "order_number": 3},
            {"option_text": f"A hypothetical exception with no practical relevance to {topic}", "is_correct": False, "order_number": 4},
        ]
    elif diff == "Hard":
        q_text = f"Under complex edge conditions in {topic}, which of the following statements is logically valid?"
        opts = [
            {"option_text": f"Boundary conditions dictate asymptotic behavior in accordance with {topic} theorems", "is_correct": True, "order_number": 1},
            {"option_text": f"The standard laws of {topic} break down completely in all scenarios", "is_correct": False, "order_number": 2},
            {"option_text": f"All initial parameters remain static and invariant regardless of input in {topic}", "is_correct": False, "order_number": 3},
            {"option_text": f"No definitive mathematical or physical model can be formulated for {topic}", "is_correct": False, "order_number": 4},
        ]
    else:  # Medium
        q_text = f"Which of the following best describes the standard analytical method in {topic}?"
        opts = [
            {"option_text": f"Systematic application of governing equations and properties in {topic}", "is_correct": True, "order_number": 1},
            {"option_text": f"Arbitrary estimation without considering variable dependencies in {topic}", "is_correct": False, "order_number": 2},
            {"option_text": f"Elimination of all known parameters in {topic}", "is_correct": False, "order_number": 3},
            {"option_text": f"Assuming constant zero outcomes for every problem in {topic}", "is_correct": False, "order_number": 4},
        ]

    return {
        "question_text": q_text,
        "question_type": "mcq",
        "difficulty": diff,
        "marks": 4,
        "order_number": order_number,
        "is_approved": True,
        "options": opts
    }


def generate_quiz_question_bank(
    module_title: str,
    module_description: str = "",
    count: int = 30
) -> list[dict]:
    """
    Generates a question bank of MCQs (default 30: 10 Easy, 10 Medium, 10 Hard).
    Each question has exactly 4 options, difficulty, 4 marks, and 1 correct answer.
    """
    topic = module_title.strip() or "Subject Topic"
    questions = []

    # Distribution: 10 Easy, 10 Medium, 10 Hard
    easy_templates = [
        ("What is the primary objective when studying {topic}?", "To understand foundational mechanics and properties", "To memorize arbitrary numbers", "To ignore variable constraints", "To eliminate all equations"),
        ("In the context of {topic}, what does a positive rate of change indicate?", "An increasing progression over time or input", "A strictly decreasing state", "Zero movement or change", "An undefined discontinuity"),
        ("Which term best describes the core unit or baseline parameter in {topic}?", "Fundamental standard unit", "Arbitrary constant", "Non-linear divisor", "Inverse reciprocal zero"),
        ("What is the initial step when solving a standard problem in {topic}?", "Identify known and unknown variables", "Assume the answer is zero", "Discard problem constraints", "Invert all equations immediately"),
        ("Which of the following is an elementary property observed in {topic}?", "Conservation and balance of parameters", "Unbounded random error", "Inconsistent mathematical definitions", "Spontaneous annihilation"),
        ("How is the baseline state in {topic} conventionally represented?", "Standard reference equilibrium", "Zero-confidence state", "Infinite divergence", "Non-computable range"),
        ("What is the simplest representation of a relationship in {topic}?", "Linear direct correlation", "Chaotic non-deterministic map", "Undefined matrix", "Random sample set"),
        ("In {topic}, what happens when input variables approach their lower limit?", "The system stabilizes toward its minimum threshold", "The system instantly diverges to infinity", "Calculations become illegal", "Variables turn into constants"),
        ("Which tool or visual representation is commonly used to introduce {topic}?", "Coordinate graphs and diagrams", "Random number tables", "Unlabeled histograms", "Blank schematics"),
        ("Why is {topic} considered a prerequisite for advanced modules?", "It establishes fundamental rules and terminology", "It has no practical value", "It cannot be analyzed mathematically", "It replaces all other subject areas"),
    ]

    medium_templates = [
        ("How do secondary variables influence the primary outcome in {topic}?", "They modulate response amplitude according to governing coefficients", "They have zero impact under any circumstance", "They cause immediate system failure", "They invert the laws of physics or logic"),
        ("When applying intermediate theorems in {topic}, what condition must be met?", "Continuous validity within the defined operational domain", "Variables must all equal 1", "Total marks must equal zero", "The equation must contain no constants"),
        ("What is the effect of scaling the primary parameter by a factor of 2 in {topic}?", "The outcome scales proportionally based on linearity or power laws", "The result is divided by zero", "No change occurs whatsoever", "The system becomes indeterminate"),
        ("Which analytical technique is optimal for isolating unknown factors in {topic}?", "Algebraic substitution and elimination", "Random guessing", "Ignoring secondary constraints", "Assuming equality of unrelated values"),
        ("In comparative analysis of {topic}, how are competing models differentiated?", "By predictive accuracy and domain applicability", "By alphabetical order of author names", "By random selection", "By whichever is shorter to write"),
        ("What distinguishes transient response from steady-state behavior in {topic}?", "Transient represents initial settling; steady-state is long-term stability", "Transient is permanent; steady-state is temporary", "Both terms are identical in meaning", "Neither applies to real systems"),
        ("How are error tolerances conventionally evaluated in {topic}?", "Measuring deviation between theoretical and empirical values", "Rounding all answers to zero", "Assuming measurements are perfectly flawless", "Ignoring experimental bounds"),
        ("Which parameter controls sensitivity and rate of convergence in {topic}?", "The damping factor or proportionality constant", "The page number of the textbook", "The student ID number", "The arbitrary offset variable"),
        ("When two interacting components in {topic} reach equilibrium, what is true?", "Net opposing forces or rates are balanced", "All energy is destroyed", "The system ceases to exist", "Values become infinite"),
        ("What is the primary risk of neglecting boundary constraints in {topic}?", "Obtaining non-physical or divergent mathematical solutions", "Nothing, constraints are optional", "Over-simplifying the problem safely", "Guaranteed 100% test accuracy"),
    ]

    hard_templates = [
        ("In multi-variable optimization within {topic}, which method guarantees finding local extrema?", "Gradient ascent/descent with appropriate learning rates", "Trial and error with 2 iterations", "Setting all partial derivatives to infinity", "Assuming the boundary is always the global optimum"),
        ("When analyzing high-order non-linear perturbations in {topic}, what behavior emerges?", "Harmonic resonance and bifurcation patterns", "Completely static linear decay", "Predictable zero-variance states", "Instantaneous return to trivial solutions"),
        ("Under asymptotic limits in {topic}, how does the error function asymptotically scale?", "Inversely with sample size or exponential decay factor", "Linearly toward infinity without bound", "It oscillates with zero frequency", "It collapses to an imaginary number"),
        ("Which mathematical formulation correctly couples dependent state vectors in {topic}?", "Coupled differential state-space matrices", "Simple arithmetic sum of scalar magnitudes", "Unchecked boolean logic gates", "Random vector products"),
        ("What is the physical or logical interpretation of eigenvalues in {topic} systems?", "System stability modes and characteristic frequencies", "Arbitrary scaling constants with no significance", "The total number of quiz questions", "The elapsed time limit of the module"),
        ("How does stochastic noise propagate through a non-linear network in {topic}?", "Non-linearly distorting variance across higher moments", "Noise is always eliminated instantaneously", "Noise causes deterministic linear amplification only", "Noise has no mathematical effect"),
        ("In advanced sensitivity analysis of {topic}, what does the Jacobian matrix represent?", "First-order partial derivatives representing localized gradients", "The determinant of arbitrary integers", "A list of quiz options", "The inverse total score"),
        ("What prevents unbounded resonance when an external driving force matches natural frequency in {topic}?", "System damping and non-linear energy dissipation", "Ignoring the external driving force", "Assuming zero mass or resistance", "Dividing by the natural frequency"),
        ("When solving ill-conditioned inverse problems in {topic}, which regularization is essential?", "Tikhonov regularization or ridge penalization", "Deleting problematic matrix rows", "Setting the condition number to zero", "Ignoring observation vectors"),
        ("How does thermodynamic or logical entropy constrain irreversible processes in {topic}?", "Non-negative entropy generation imposes directional irreversibility", "Entropy can decrease to negative infinity in closed systems", "Entropy only applies to chemistry, not {topic}", "Entropy guarantees 100% energy recovery"),
    ]

    order = 1
    # 10 Easy
    for tmpl in easy_templates[:10]:
        q_text = tmpl[0].format(topic=topic)
        questions.append({
            "question_text": q_text,
            "question_type": "mcq",
            "difficulty": "Easy",
            "marks": 4,
            "order_number": order,
            "is_approved": True,
            "options": [
                {"option_text": tmpl[1], "is_correct": True, "order_number": 1},
                {"option_text": tmpl[2], "is_correct": False, "order_number": 2},
                {"option_text": tmpl[3], "is_correct": False, "order_number": 3},
                {"option_text": tmpl[4], "is_correct": False, "order_number": 4},
            ]
        })
        order += 1

    # 10 Medium
    for tmpl in medium_templates[:10]:
        q_text = tmpl[0].format(topic=topic)
        questions.append({
            "question_text": q_text,
            "question_type": "mcq",
            "difficulty": "Medium",
            "marks": 4,
            "order_number": order,
            "is_approved": True,
            "options": [
                {"option_text": tmpl[1], "is_correct": True, "order_number": 1},
                {"option_text": tmpl[2], "is_correct": False, "order_number": 2},
                {"option_text": tmpl[3], "is_correct": False, "order_number": 3},
                {"option_text": tmpl[4], "is_correct": False, "order_number": 4},
            ]
        })
        order += 1

    # 10 Hard
    for tmpl in hard_templates[:10]:
        q_text = tmpl[0].format(topic=topic)
        questions.append({
            "question_text": q_text,
            "question_type": "mcq",
            "difficulty": "Hard",
            "marks": 4,
            "order_number": order,
            "is_approved": True,
            "options": [
                {"option_text": tmpl[1], "is_correct": True, "order_number": 1},
                {"option_text": tmpl[2], "is_correct": False, "order_number": 2},
                {"option_text": tmpl[3], "is_correct": False, "order_number": 3},
                {"option_text": tmpl[4], "is_correct": False, "order_number": 4},
            ]
        })
        order += 1

    return questions[:count]
