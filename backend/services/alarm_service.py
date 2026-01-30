from core.llm import generate_llm
from utils.text_utils import normalize_steps, clean_llm_output
from services.excel_loader import vectorstore, extract_description_only


def handle_alarm_code(alarm_code: str):
    docs = vectorstore.similarity_search(
        alarm_code, k=1, filter={"alarm_no": alarm_code}
    )

    if not docs:
        return {"reply": f"No data found for alarm {alarm_code}."}

    desc = extract_description_only(docs[0].page_content)

    prompt = f"""
You are an industrial maintenance engineer.
Generate corrective actions.

Alarm Description:
{desc}

Actions:
"""
    solution = normalize_steps(
        clean_llm_output(generate_llm(prompt))
    )

    return {
        "reply": (
            f"Alarm Number: {alarm_code}\n"
            f"Alarm Description: {desc}\n"
            f"Solution:\n{solution}"
        )
    }


def handle_alarm_description(text: str):
    docs = vectorstore.similarity_search(text, k=1)

    if not docs:
        return None

    desc = extract_description_only(docs[0].page_content)

    prompt = f"""
You are an industrial maintenance engineer.
Generate corrective actions.

Alarm Description:
{desc}

Actions:
"""
    solution = normalize_steps(
        clean_llm_output(generate_llm(prompt))
    )

    return {"reply": solution}
