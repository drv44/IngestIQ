# app/main.py
import io
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .agents.classifier_agent import ClassifierAgent
from .agents.json_agent import JSONAgent
from .agents.email_agent import EmailAgent
from .memory.memory_manager import MemoryManager

app = FastAPI()
memory = MemoryManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return "API Running!!!"

@app.post("/process")
async def process_document(file: UploadFile = File(...), conversation_id: str = None):
    content = await file.read()
    
    # Handle PDF conversion
    if file.filename.endswith(".pdf"):
        from PyPDF2 import PdfReader
        pdf = PdfReader(io.BytesIO(content))
        content = "\n".join([page.extract_text() for page in pdf.pages])
    else:
        content = content.decode("utf-8")
    
    # Classify document
    classifier = ClassifierAgent(memory)

    # Set context if continuing conversation
    if conversation_id:
        classifier.set_context(conversation_id)

    classification = classifier.classify(content, file.filename)
    
    # Route to appropriate agent
    if classification.format == "JSON":
        agent = JSONAgent(memory)
        agent.set_context(classification.conversation_id)
        result = agent.process(content, classification.conversation_id)
    else:  # Email/PDF
        agent = EmailAgent(memory)
        agent.set_context(classification.conversation_id)
        result = agent.extract_info(content, classification.conversation_id)
    
    return {
        "conversation_id": classification.conversation_id,
        "result": result
    }

@app.get("/context/{conv_id}")
def get_context(conv_id: str):
    return memory.get_entry(conv_id)