from retrieval.retriever import Retriever
from llm.generator import LLMGenerator
from llm.intent_detector import IntentDetector


class RAGPipeline:

    def __init__(self):

        self.retriever = Retriever(top_k=5)
        self.generator = LLMGenerator()
        self.intent_detector = IntentDetector()

        # Conversation memory
        self.previous_question = None
        self.previous_answer = None
        self.previous_context = None

    def answer(self, question, class_name=None, subject=None):

        # ==========================================
        # 1. Detect student intent
        # ==========================================

        intent_result = self.intent_detector.detect_intent(
            current_message=question,
            previous_question=self.previous_question,
            previous_answer=self.previous_answer
        )

        intent = intent_result.get("intent", "new_question")

        print(f"\n[Intent: {intent}]")

        # ==========================================
        # 2. Greeting
        # ==========================================

        if intent == "greeting":

            return (
                "Hello! 😊\n"
                "I'm your EduBridge AI Tutor. "
                "Ask me anything from your study material."
            )

        # ==========================================
        # 3. Clarification
        # ==========================================

        if (
            intent == "clarification"
            and self.previous_answer
        ):

            clarification_prompt = f"""
The student did not understand the previous explanation.

Previous question:
{self.previous_question}

Previous answer:
{self.previous_answer}

Student's new message:
{question}

Explain the SAME concept again.

Important:
- Do not assume what part confused the student.
- Give a different and simpler explanation.
- Use very easy language.
- Use short sentences.
- Use a simple example or analogy if useful.
- Do not introduce unrelated information.
- Stay within the study material.
"""

            answer = self.generator.generate(
                clarification_prompt,
                self.previous_context
            )

            self.previous_answer = answer

            return answer

        # ==========================================
        # 4. Follow-up question
        # ==========================================

        if (
            intent == "follow_up"
            and self.previous_answer
        ):

            follow_up_prompt = f"""
The student is asking a follow-up question about the
previous topic.

Previous question:
{self.previous_question}

Previous answer:
{self.previous_answer}

Student's follow-up question:
{question}

Answer the student's follow-up question.

Important:
- Understand what words such as "it", "this", "that",
  "this process", or "they" refer to using the previous
  conversation.
- Do NOT ask the student to repeat the topic if the
  previous conversation gives enough context.
- Answer directly.
- Use simple language suitable for a school student.
- Stay grounded in the provided study material.
"""

            answer = self.generator.generate(
                follow_up_prompt,
                self.previous_context
            )

            self.previous_answer = answer

            return answer

        # ==========================================
        # 5. Example request
        # ==========================================

        if (
            intent == "example_request"
            and self.previous_answer
        ):

            example_prompt = f"""
The student wants an example related to the previous topic.

Previous question:
{self.previous_question}

Previous answer:
{self.previous_answer}

Student's request:
{question}

Give a simple, easy-to-understand example.

Use the previous topic as context.
Do not change the topic.
"""

            answer = self.generator.generate(
                example_prompt,
                self.previous_context
            )

            self.previous_answer = answer

            return answer

        # ==========================================
        # 6. Summary request
        # ==========================================

        if (
            intent == "summary_request"
            and self.previous_answer
        ):

            summary_prompt = f"""
The student wants a short summary of the previous explanation.

Previous question:
{self.previous_question}

Previous answer:
{self.previous_answer}

Student's request:
{question}

Give the answer in 1-3 simple sentences.
Keep only the most important points.
"""

            answer = self.generator.generate(
                summary_prompt,
                self.previous_context
            )

            self.previous_answer = answer

            return answer

        # ==========================================
        # 7. NEW QUESTION
        # ==========================================

        results = self.retriever.retrieve(
            question,
            class_name=class_name,
            subject=subject
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        # ==========================================
        # 8. Build context
        # ==========================================

        context_parts = []

        for i, document in enumerate(documents):

            metadata = metadatas[i]

            context_parts.append(
                f"""
Source: {metadata['source']}
Class: {metadata['class']}
Subject: {metadata['subject']}

{document}
"""
            )

        context = "\n\n".join(context_parts)

        # ==========================================
        # 9. Generate answer
        # ==========================================

        answer = self.generator.generate(
            question,
            context
        )

        # ==========================================
        # 10. Save conversation memory
        # ==========================================

        self.previous_question = question
        self.previous_answer = answer
        self.previous_context = context

        return answer


# ==================================================
# Run chatbot
# ==================================================

if __name__ == "__main__":

    rag = RAGPipeline()

    print("\n===== EduBridge AI Tutor =====")

    # Student selects class
    class_name = input(
        "Enter class (example: class8, class9, class10): "
    ).strip().lower()

    # Student selects subject
    subject = input(
        "Enter subject (example: science, maths, social): "
    ).strip().lower()

    print("\nType 'exit' to stop.\n")

    while True:

        question = input("Student: ")

        if question.lower().strip() == "exit":
            break

        answer = rag.answer(
            question,
            class_name=class_name,
            subject=subject
        )

        print("\nTutor:")
        print(answer)
        print()