# core/llm.py

import os
from llama_cpp import Llama

# ===============================
# RESOLVE BASE DIRECTORY
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "tinyllama.gguf"
)

# ===============================
# LLM ENGINE
# ===============================
class LLMEngine:
    def __init__(self, model_path: str):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"LLM model not found at: {model_path}")

        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4,
            n_batch=128,
            verbose=False
        )

        # Warm-up
        self.llm("Hello", max_tokens=1)

    def generate(self, prompt: str, max_tokens: int = 220) -> str:
        result = self.llm(
            prompt,
            max_tokens=max_tokens,
            stop=["System:", "User:", "Assistant:"]
        )
        return result["choices"][0]["text"].strip()


# ===============================
# SINGLETON INSTANCE
# ===============================
_llm_engine = None


def get_llm_engine() -> LLMEngine:
    global _llm_engine
    if _llm_engine is None:
        _llm_engine = LLMEngine(MODEL_PATH)
    return _llm_engine


# ===============================
# PUBLIC FUNCTION
# ===============================
def generate_llm(prompt: str, max_tokens: int = 220) -> str:
    return get_llm_engine().generate(prompt, max_tokens)
