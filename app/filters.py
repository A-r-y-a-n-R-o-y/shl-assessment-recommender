import re


class MetadataFilter:
    """
    Filters retrieved assessments using metadata extracted
    from the user's query.
    """

    def apply(self, query: str, results: list):

        query = query.lower()

        filtered = results

        # ------------------------------------
        # Job Level Filtering
        # ------------------------------------

        job_level_map = {
            "graduate": "Graduate",
            "intern": "Entry",
            "entry": "Entry",
            "junior": "Entry",
            "mid": "Mid",
            "mid-level": "Mid",
            "mid level": "Mid",
            "senior": "Professional",
            "manager": "Manager",
            "executive": "Executive"
        }

        requested_levels = []

        for keyword, level in job_level_map.items():
            if keyword in query:
                requested_levels.append(level)

        if requested_levels:

            temp = []

            for item in filtered:

                levels = " ".join(item.get("job_levels", [])).lower()

                if any(level.lower() in levels for level in requested_levels):
                    temp.append(item)

            if temp:
                filtered = temp

        # ------------------------------------
        # Categories
        # ------------------------------------

        category_map = {
            "personality": "Personality",
            "behavior": "Personality",
            "behaviour": "Personality",
            "cognitive": "Ability",
            "ability": "Ability",
            "aptitude": "Ability",
            "skill": "Knowledge",
            "technical": "Knowledge",
            "knowledge": "Knowledge"
        }

        requested_categories = []

        for keyword, category in category_map.items():
            if keyword in query:
                requested_categories.append(category)

        if requested_categories:

            temp = []

            for item in filtered:

                cats = " ".join(item.get("categories", [])).lower()

                if any(cat.lower() in cats for cat in requested_categories):
                    temp.append(item)

            if temp:
                filtered = temp

        # ------------------------------------
        # Remote Testing
        # ------------------------------------

        if "remote" in query or "online" in query:

            temp = []

            for item in filtered:

                remote = str(item.get("remote", "")).lower()

                if "yes" in remote or "true" in remote:
                    temp.append(item)

            if temp:
                filtered = temp

        # ------------------------------------
        # Adaptive
        # ------------------------------------

        if "adaptive" in query:

            temp = []

            for item in filtered:

                adaptive = str(item.get("adaptive", "")).lower()

                if "yes" in adaptive or "true" in adaptive:
                    temp.append(item)

            if temp:
                filtered = temp

        # ------------------------------------
        # Duration
        # ------------------------------------

        match = re.search(r"(\d+)\s*minutes?", query)

        if match:

            max_duration = int(match.group(1))

            temp = []

            for item in filtered:

                duration = str(item.get("duration", ""))

                number = re.search(r"\d+", duration)

                if number:

                    if int(number.group()) <= max_duration:
                        temp.append(item)

            if temp:
                filtered = temp

        return filtered