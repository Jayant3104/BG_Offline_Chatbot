import os
import pandas as pd

from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(BASE_DIR, "data", "data.xlsx")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

# --- Vector Store ---
embedding = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embedding
)


def load_excel_to_chroma():
    if not os.path.exists(EXCEL_PATH):
        return

    df = pd.read_excel(EXCEL_PATH)
    docs = []

    for _, row in df.iterrows():
        alarm_no = str(row["Alarm No."]).strip().upper()
        desc = str(row["Alarm Description"]).strip()
        sol = str(row.get("Solution", "")).strip() or "NO_SOLUTION"

        docs.append(
            Document(
                page_content=(
                    f"Alarm Number: {alarm_no}\n"
                    f"Alarm Description: {desc}\n"
                    f"Solution: {sol}"
                ),
                metadata={"alarm_no": alarm_no}
            )
        )

    vectorstore.add_documents(docs)


def extract_description_only(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("Alarm Description:"):
            return line.replace("Alarm Description:", "").strip()
    return ""
