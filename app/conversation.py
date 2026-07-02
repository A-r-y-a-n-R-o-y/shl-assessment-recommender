from typing import List


class ConversationAnalyzer:
    """
    Determines what action the agent should take
    based on the conversation history.
    """

    def analyze(self, messages: List):

        # Latest user message
        latest = ""

        for msg in reversed(messages):
            if msg.role == "user":
                latest = msg.content.lower().strip()
                break

        # -------------------------
        # Comparison
        # -------------------------

        compare_words = [
            "compare",
            "difference",
            "vs",
            "versus"
        ]

        if any(word in latest for word in compare_words):
            return "compare"

        # -------------------------
        # Refinement
        # -------------------------

        refine_words = [
            "actually",
            "instead",
            "also",
            "add",
            "remove",
            "change"
        ]

        if any(word in latest for word in refine_words):
            return "refine"

        # -------------------------
        # Recommendation
        # -------------------------

        refine_words = [
            "actually",
            "instead",
            "also",
            "add",
            "remove",
            "change"
            "only",
            "exclude",
            "include",
            "more",
            "less",
            "senior",
            "junior",
            "mid",
            "graduate",
            "cloud",
            "python",
            "java",
            "manager",
            "sales"
        ]

        if any(word in latest for word in role_words):
            return "recommend"

        # -------------------------
        # Clarification
        # -------------------------

        return "clarify"