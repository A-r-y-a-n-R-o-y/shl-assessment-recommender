class Guardrails:

    OFF_TOPIC_KEYWORDS = [
        "weather",
        "cricket",
        "football",
        "ipl",
        "movie",
        "netflix",
        "recipe",
        "travel",
        "restaurant",
        "stock market",
        "bitcoin",
        "politics",
        "news"
    ]

    LEGAL_KEYWORDS = [
        "legal",
        "law",
        "lawsuit",
        "contract",
        "sue",
        "court",
        "gdpr",
        "compliance"
    ]

    HIRING_ADVICE_KEYWORDS = [
        "salary",
        "fire employee",
        "terminate employee",
        "promotion",
        "promotion policy",
        "hr policy",
        "interview questions",
        "offer letter",
        "resume review"
    ]

    PROMPT_INJECTION_KEYWORDS = [
        "ignore previous instructions",
        "ignore your instructions",
        "system prompt",
        "developer message",
        "reveal your prompt",
        "act as",
        "pretend to be",
        "jailbreak"
    ]

    def check(self, text: str):
        """
        Returns:
        None -> request is allowed
        dict -> refusal response
        """

        query = text.lower()

        # Prompt injection
        if any(k in query for k in self.PROMPT_INJECTION_KEYWORDS):
            return {
                "reply": (
                    "I can only assist with recommending and comparing SHL assessments "
                    "using the official SHL product catalog."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # Legal
        if any(k in query for k in self.LEGAL_KEYWORDS):
            return {
                "reply": (
                    "I'm only able to help with SHL assessment recommendations and "
                    "comparisons. I can't provide legal guidance."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # General hiring advice
        if any(k in query for k in self.HIRING_ADVICE_KEYWORDS):
            return {
                "reply": (
                    "I can help recommend SHL assessments for hiring and talent "
                    "evaluation, but I can't provide general HR or hiring advice."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # Off-topic
        if any(k in query for k in self.OFF_TOPIC_KEYWORDS):
            return {
                "reply": (
                    "I'm designed specifically to recommend and compare SHL "
                    "assessments. Please ask me about SHL assessments or hiring "
                    "assessment selection."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        return None