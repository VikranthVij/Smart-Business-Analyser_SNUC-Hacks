def apply_guardrails(response):
    banned = ["maybe", "could", "it depends", "not sure"]

    for word in banned:
        if word in response.lower():
            return False, "Vague output detected"

    required_sections = [
        "Strategy:",
        "Messaging:",
        "Execution Steps:",
        "Reasoning:"
    ]

    for sec in required_sections:
        if sec not in response:
            return False, f"Missing section: {sec}"

    if len(response.strip()) < 100:
        return False, "Too short output"

    return True, response