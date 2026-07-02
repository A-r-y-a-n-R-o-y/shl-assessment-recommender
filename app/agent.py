from app.retrieval import HybridRetriever
from app.conversation import ConversationAnalyzer
from app.llm import LLM
from app.prompts import build_recommendation_prompt
from app.guardrails import Guardrails
from app.filters import MetadataFilter


class SHLAgent:
    def __init__(self):
        self.retriever = HybridRetriever()
        self.analyzer = ConversationAnalyzer()
        self.llm = LLM()
        self.guardrails = Guardrails()
        self.filter = MetadataFilter()

    def process(self, messages):
        """
        Main conversational entry point.
        """

        # ----------------------------------------------------
        # Latest user message
        # ----------------------------------------------------

        latest_message = ""

        for msg in reversed(messages):
            if msg.role == "user":
                latest_message = msg.content.strip()
                break

        if not latest_message:
            return {
                "reply": "How can I help you find an SHL assessment?",
                "recommendations": [],
                "end_of_conversation": False,
            }

        # ----------------------------------------------------
        # Guardrails
        # ----------------------------------------------------

        guardrail_response = self.guardrails.check(latest_message)

        if guardrail_response:
            return guardrail_response

        # ----------------------------------------------------
        # Intent Detection
        # ----------------------------------------------------

        intent = self.analyzer.analyze(messages)

        # ----------------------------------------------------
        # Clarification
        # ----------------------------------------------------

        if intent == "clarify":
            return {
                "reply": (
                    "I'd be happy to help you choose the right SHL assessment. "
                    "Could you tell me more about the role you're hiring for? "
                    "For example, the job title, seniority level, required skills, "
                    "or whether you're looking for technical, cognitive, personality, "
                    "or behavioral assessments."
                ),
                "recommendations": [],
                "end_of_conversation": False,
            }

        # ----------------------------------------------------
        # Build Search Query
        # ----------------------------------------------------

        search_query = latest_message

        if intent == "refine":

            previous_queries = [
                msg.content.strip()
                for msg in messages
                if msg.role == "user"
            ]

            if len(previous_queries) >= 2:
                search_query = " ".join(previous_queries)

        # ----------------------------------------------------
        # Retrieve Assessments
        # ----------------------------------------------------

        results = self.retriever.search(search_query, top_k=50)

        # ----------------------------------------------------
        # Metadata Filtering
        # ----------------------------------------------------

        results = self.filter.apply(search_query, results)

        if not results:
            return {
                "reply": (
                    "I couldn't find any matching SHL assessments. "
                    "Could you provide more details about the role, required skills, "
                    "or assessment type?"
                ),
                "recommendations": [],
                "end_of_conversation": False,
            }

        # Keep top recommendations after filtering
        results = results[:5]

        # ----------------------------------------------------
        # Build Recommendation Objects
        # ----------------------------------------------------

        recommendations = []

        for item in results:

            categories = item.get("categories", [])

            recommendations.append(
                {
                    "name": item.get("name", ""),
                    "url": item.get("url", ""),
                    "test_type": categories[0] if categories else "Unknown",
                }
            )

        # ----------------------------------------------------
        # Comparison Prompt
        # ----------------------------------------------------

        if intent == "compare":

            prompt = f"""
You are an SHL Assessment expert.

User request:
{latest_message}

Compare ONLY the following assessments.

"""

            for assessment in results:

                prompt += f"""
Name: {assessment.get("name","")}
Description: {assessment.get("description","")}
Categories: {", ".join(assessment.get("categories", []))}
Job Levels: {", ".join(assessment.get("job_levels", []))}
Languages: {", ".join(assessment.get("languages", []))}
Duration: {assessment.get("duration","")}
Remote Testing: {assessment.get("remote","")}
Adaptive: {assessment.get("adaptive","")}
URL: {assessment.get("url","")}

"""

            prompt += """
Instructions:

- Compare the assessments.
- Mention strengths.
- Mention limitations.
- Mention ideal hiring scenarios.
- Highlight important differences.
- Recommend when each should be selected.
- Do NOT invent information.
- Use only the provided assessment data.
- Keep the answer under 150 words.
"""

            reply = self.llm.generate(prompt)

        # ----------------------------------------------------
        # Recommendation / Refinement
        # ----------------------------------------------------

        else:

            prompt = build_recommendation_prompt(
                search_query,
                results,
            )

            reply = self.llm.generate(prompt)

        # ----------------------------------------------------
        # Final Response
        # ----------------------------------------------------

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": True,
        }