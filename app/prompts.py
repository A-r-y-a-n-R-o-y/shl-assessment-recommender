def build_recommendation_prompt(user_query: str, assessments: list) -> str:
    """
    Builds a grounded prompt for Gemini.
    Gemini must answer ONLY using the retrieved SHL catalog entries.
    """

    catalog_context = ""

    for i, assessment in enumerate(assessments, start=1):

        catalog_context += f"""
Assessment {i}
Name: {assessment.get("name", "")}
Description: {assessment.get("description", "")}
Categories: {", ".join(assessment.get("categories", []))}
Job Levels: {", ".join(assessment.get("job_levels", []))}
Duration: {assessment.get("duration", "Not specified")}
Remote Testing: {assessment.get("remote", "Unknown")}
URL: {assessment.get("url", "")}

"""

    return f"""
You are an expert SHL Assessment Recommendation Assistant.

You MUST answer ONLY from the assessments below.

User Request:
{user_query}

Retrieved SHL Assessments:
{catalog_context}

Instructions:
- Recommend only from the retrieved assessments.
- Briefly explain why they fit.
- Do not invent assessments.
- Do not invent features.
- Mention assessment names exactly as provided.
- Keep the response under 150 words.
"""