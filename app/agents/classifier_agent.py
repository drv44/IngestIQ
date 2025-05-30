# app/agents/classifier_agent.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from ..memory.memory_manager import MemoryManager
from ..schemas import ClassificationResult

load_dotenv()

class ClassifierAgent:
    def __init__(self, memory: MemoryManager):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.memory = memory
        self.context = None
    
    def set_context(self, conv_id: str):
        """Set the current working context from memory"""
        self.context = self.memory.get_entry(conv_id)

    def classify(self, content: str, filename: str) -> ClassificationResult:
        # Use context if available
        context_str = ""
        if self.context:
            context_str = f"\n\n[CONTEXT]\nPrevious intent: {self.context.get('intent')}\nExtracted fields: {self.context.get('extracted_fields', {}).keys()}"

        prompt = f"""
        Classify the document:
        Format: [PDF/JSON/Email]
        Intent: [Invoice/RFQ/Complaint/Regulation/Other]
        Content: {content[:5000]}
        {context_str}
        """
        response = self.model.generate_content(prompt)
        
        # Extract classification from response
        format = "Email" if "email" in response.text.lower() else "PDF" if "pdf" in response.text.lower() else "JSON"
        intent = next((i for i in ["Invoice", "RFQ", "Complaint", "Regulation"] if i in response.text), "Other")
        
        # Store in memory
        conv_id = self.memory.create_entry(
            source=filename,
            format=format,
            intent=intent
        )
        return ClassificationResult(format=format, intent=intent, conversation_id=conv_id)

