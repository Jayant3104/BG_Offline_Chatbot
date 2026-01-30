import re

def clean_llm_output(text: str) -> str:
    banned = [
        "Alarm Number", "Alarm Description", "Solution",
        "Context", "Rule", "Rules"
    ]
    for b in banned:
        text = text.replace(b, "")

    seen = set()
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line and line.lower() not in seen:
            seen.add(line.lower())
            lines.append(line)

    return "\n".join(lines).strip()


def normalize_steps(text: str) -> str:
    steps, seen = [], set()

    for line in text.splitlines():
        line = re.sub(r"^[\d\.\-\)\:]+", "", line).strip()
        if len(line) < 8:
            continue
        if line.lower().startswith(("if ", "when ", "else")):
            continue
        if line.lower() in seen:
            continue

        seen.add(line.lower())
        steps.append(line)
        if len(steps) == 5:
            break

    fallback = [
        "Inspect the affected component for physical damage.",
        "Verify electrical and mechanical connections.",
        "Check sensor signals and controller feedback.",
        "Replace the faulty component if required.",
        "Reset the alarm and monitor system operation."
    ]

    while len(steps) < 5:
        steps.append(fallback[len(steps)])

    return "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))


def extract_description(text: str) -> str:
    match = re.search(r"Alarm Description:\s*(.*)", text)
    return match.group(1).strip() if match else ""
