import os
import json
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv(Path(__file__).resolve().parents[2] / ".env")
load_dotenv(Path(__file__).resolve().parents[1] / ".env")
load_dotenv()


class IntentDetector:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env")

        self.client = Groq(api_key=api_key)
        self.model = "openai/gpt-oss-120b"

    def detect_intent(
        self,
        current_message,
        previous_question=None,
        previous_answer=None
    ):

        current = current_message.strip().lower()

        # ==========================================
        # No previous conversation
        # ==========================================

        if not previous_question:
            return self._ask_groq(
                current_message,
                previous_question,
                previous_answer
            )

        # ==========================================
        # Obvious clarification messages
        # ==========================================

        clarification_phrases = [
            "i don't understand",
            "i dont understand",
            "i didn't understand",
            "i didnt understand",
            "i don't get it",
            "i dont get it",
            "i didn't get it",
            "i didnt get it",
            "i'm confused",
            "im confused",
            "i am confused",
            "explain again",
            "explain that again",
            "explain differently",
            "explain it differently",
            "make it easier",
            "make that easier",
            "make it simple",
            "explain simply",
            "explain in simple words",
            "explain in easy words"
        ]

        if any(
            phrase in current
            for phrase in clarification_phrases
        ):

            return {
                "intent": "clarification"
            }

        # ==========================================
        # Obvious example requests
        # ==========================================

        example_phrases = [
            "give me an example",
            "give an example",
            "can you give an example",
            "example please"
        ]

        if any(
            phrase in current
            for phrase in example_phrases
        ):

            return {
                "intent": "example_request"
            }

        # ==========================================
        # Obvious summary requests
        # ==========================================

        summary_phrases = [
            "summarize",
            "summarise",
            "in two lines",
            "in one line",
            "short answer",
            "short explanation",
            "make it short",
            "briefly"
        ]

        if any(
            phrase in current
            for phrase in summary_phrases
        ):

            return {
                "intent": "summary_request"
            }

        # ==========================================
        # Obvious contextual follow-up questions
        # ==========================================

        follow_up_phrases = [
            "why is it",
            "why it is",
            "why does it",
            "why do they",
            "why do we",
            "how does it",
            "how do they",
            "how does this",
            "how does that",
            "what does it",
            "what do they",
            "what is its",
            "what are its",
            "where does it",
            "where is it",
            "when does it",
            "what happens next",
            "what happens after that",
            "what happens after this"
        ]

        if any(
            phrase in current
            for phrase in follow_up_phrases
        ):

            return {
                "intent": "follow_up"
            }

        # ==========================================
        # Very short dependent questions
        # ==========================================

        words = current.split()

        reference_words = [
            "it",
            "its",
            "this",
            "that",
            "they",
            "them",
            "these",
            "those"
        ]

        if (
            len(words) <= 8
            and any(word in words for word in reference_words)
            and "?" in current_message
        ):

            return {
                "intent": "follow_up"
            }

        # ==========================================
        # Let Groq classify everything else
        # ==========================================

        return self._ask_groq(
            current_message,
            previous_question,
            previous_answer
        )

    # ==============================================
    # Groq Intent Classification
    # ==============================================

    def _ask_groq(
        self,
        current_message,
        previous_question,
        previous_answer
    ):

        prompt = f"""
You are an intent classifier for an educational AI tutor.

Possible intents:

new_question
clarification
follow_up
example_request
summary_request
greeting
other

Previous question:
{previous_question}

Previous answer:
{previous_answer}

Current student message:
{current_message}

Rules:

1. new_question:
The student asks about a new topic.

Example:
Previous question: What is photosynthesis?
Current: What is respiration?

2. clarification:
The student says they do not understand the previous explanation
or wants it explained differently.

Example:
"I still don't understand."

3. follow_up:
The student asks something connected to the previous topic.

Example:
Previous question: What is photosynthesis?
Current: Why is it important?

Example:
Previous question: What is photosynthesis?
Current: How does it work?

4. example_request:
The student asks for an example.

5. summary_request:
The student asks for a short or summarized explanation.

6. greeting:
The student is greeting the tutor.

IMPORTANT:

Consider the previous conversation.

If the current message depends on the previous topic,
use follow_up.

Return ONLY JSON.

Example:
{{"intent": "follow_up"}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You classify student intent accurately. "
                        "Return only valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response.choices[0].message.content.strip()

        try:

            parsed = json.loads(result)

            valid_intents = [
                "new_question",
                "clarification",
                "follow_up",
                "example_request",
                "summary_request",
                "greeting",
                "other"
            ]

            if parsed.get("intent") in valid_intents:
                return parsed

        except json.JSONDecodeError:
            pass

        return {
            "intent": "new_question"
        }


# ==================================================
# Simple test
# ==================================================

if __name__ == "__main__":

    detector = IntentDetector()

    previous_question = (
        "What is photosynthesis?"
    )

    previous_answer = (
        "Photosynthesis is the process by which green plants "
        "make their food using sunlight."
    )

    print("\n===== EduBridge Intent Detector =====")
    print("Type 'exit' to stop.\n")

    while True:

        message = input("Student: ")

        if message.lower().strip() == "exit":
            break

        result = detector.detect_intent(
            current_message=message,
            previous_question=previous_question,
            previous_answer=previous_answer
        )

        print("Detected intent:", result)