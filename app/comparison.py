import re


class ComparisonParser:
    """
    Extracts assessment names from comparison queries.

    Examples:
    - Compare OPQ and Verify Interactive
    - OPQ vs Verify Interactive
    - Difference between Java 8 and Core Java
    """

    def extract(self, text: str):
        text = text.strip()

        # compare X and Y
        m = re.search(r"compare\s+(.+?)\s+(?:and|vs|versus)\s+(.+)", text, re.I)
        if m:
            return m.group(1).strip(), m.group(2).strip()

        # difference between X and Y
        m = re.search(
            r"difference\s+between\s+(.+?)\s+and\s+(.+)",
            text,
            re.I,
        )
        if m:
            return m.group(1).strip(), m.group(2).strip()

        # X vs Y
        m = re.search(r"(.+?)\s+(?:vs|versus)\s+(.+)", text, re.I)
        if m:
            return m.group(1).strip(), m.group(2).strip()

        return None, None