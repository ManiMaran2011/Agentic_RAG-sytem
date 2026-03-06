def weighted_score(matched_requirements):

    if not matched_requirements:
        return 0

    total_weight = 0
    achieved_weight = 0

    for req in matched_requirements:

        requirement_text = str(req.get("requirement", "")).lower()
        status = str(req.get("status", "")).strip().upper()
        status = status.replace(".", "").replace(":", "")

        weight = 1

        if "insurance" in requirement_text:
            weight = 3
        elif "sam" in requirement_text:
            weight = 3
        elif "cage" in requirement_text:
            weight = 2
        elif "experience" in requirement_text:
            weight = 2

        total_weight += weight

        if status == "MET" or "MET" in status:
            achieved_weight += weight

    if total_weight == 0:
        return 0

    return round((achieved_weight / total_weight) * 100, 2)


def compliance_breakdown(matched_requirements):

    mandatory_total = 0
    mandatory_met = 0

    preferred_total = 0
    preferred_met = 0

    for req in matched_requirements:

        requirement_text = str(req.get("requirement", "")).lower()
        status = str(req.get("status", "")).strip().upper()

        is_preferred = "preferred" in requirement_text

        if is_preferred:
            preferred_total += 1
            if status == "MET" or "MET" in status:
                preferred_met += 1
        else:
            mandatory_total += 1
            if status == "MET" or "MET" in status:
                mandatory_met += 1

    mandatory_score = round(
        (mandatory_met / mandatory_total) * 100, 2
    ) if mandatory_total > 0 else 0

    preferred_score = round(
        (preferred_met / preferred_total) * 100, 2
    ) if preferred_total > 0 else 0

    return mandatory_score, preferred_score