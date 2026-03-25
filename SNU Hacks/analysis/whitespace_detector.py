def detect_whitespace(segments):
    known_segments = ["enterprise", "teams", "developers", "business"]

    whitespace = []

    for seg in ["freelancers", "students", "creators"]:
        if seg not in segments:
            whitespace.append(seg)

    return whitespace
