import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXCEL_PATH = os.path.join(BASE_DIR, "data", "data.xlsx")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")
MODEL_PATH = os.path.join(BASE_DIR, "models", "tinyllama.gguf")
