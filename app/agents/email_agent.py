# app/agents/email_agent.py
import os
import re
from dotenv import load_dotenv
import google.generativeai as genai
from ..memory.memory_manager import MemoryManager

load_dotenv()

class EmailAgent:
    def __init__(self, memory: MemoryManager):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.memory = memory
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.context = None

    def set_context(self, conv_id: str):
        self.context = self.memory.get_entry(conv_id)
    
    def extract_info(self, email_content: str, conv_id: str) -> dict:
        # Use context if available
        context_str = ""
        if self.context:
            context_str = f"\n\n[CONTEXT]\nPrevious interaction: {self.context.get('intent')}\nKnown sender: {self.context.get('extracted_fields', {}).get('sender', '')}"
            
        # Extract basic fields
        sender = re.search(r'From: (.+)', email_content).group(1) if "From:" in email_content else "Unknown"
        subject = re.search(r'Subject: (.+)', email_content).group(1) if "Subject:" in email_content else ""
        
        # Extract details with LLM
        prompt = f"""
        Extract from email:
        - Intent details
        - Urgency level [Low/Medium/High]
        - Key entities
        Email: {email_content[:10000]}
        """
        response = self.model.generate_content(prompt)
        
        # Store extracted fields
        extracted = {
            "sender": sender,
            "subject": subject,
            "urgency": "Medium",
            "details": response.text
        }
        self.memory.update_entry(conv_id, extracted_fields=extracted)
        
        return extracted