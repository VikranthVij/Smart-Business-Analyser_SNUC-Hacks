def apply_rules(context):
    output = {
        "priority_segments": [],
        "strategy_flags": []
    }

    trends = context.get("trends", [])
    whitespace = context.get("whitespace", [])
    overused = context.get("overused", [])

    # Rule 1: AI trend
    if any("AI" in t for t in trends):
        output["strategy_flags"].append("focus_on_ai")

    # Rule 2: Whitespace priority
    if whitespace:
        output["priority_segments"] = whitespace

    # Rule 3: Avoid saturation
    if len(overused) >= 2:
        output["strategy_flags"].append("avoid_generic_positioning")

    # Rule 4: Enterprise trend
    if any("enterprise" in t.lower() for t in trends):
        output["strategy_flags"].append("target_enterprise")

    return output