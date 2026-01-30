from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.chat_controller import router as chat_router
from services.excel_loader import load_excel_to_chroma

app = FastAPI(title="Beumer Alarm Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Excel data on startup
load_excel_to_chroma()

# Register routes
app.include_router(chat_router)
