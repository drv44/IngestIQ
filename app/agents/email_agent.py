import os
import re
from dotenv import load_dotenv
import google.generativeai as genai
from ..memory.memory_manager import MemoryManager

load_dotenv()

class EmailAgent:
    def __init__(self, memory: MemoryManager):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in .env")
        genai.configure(api_key=api_key)

        self.memory = memory
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.context = None

    def set_context(self, conv_id: str):
        self.context = self.memory.get_entry(conv_id)

    def extract_info(self, email_content: str, conv_id: str) -> dict:
        # Use context if available
        context_str = ""
        if self.context:
            prev_intent = self.context.get('intent', '')
            known_sender = self.context.get('extracted_fields', {}).get('sender', '')
            context_str = (
                f"\n\n[CONTEXT]\n"
                f"Previous interaction: {prev_intent}\n"
                f"Known sender: {known_sender}"
            )

        # 1. Extract sender safely
        sender = "Unknown"
        # look for a line starting with "From:" (allow any amount of whitespace after colon)
        match_from = re.search(r'From:\s*(.+)', email_content)
        if match_from:
            sender = match_from.group(1).strip()

        # 2. Extract subject safely
        subject = ""
        match_subj = re.search(r'Subject:\s*(.+)', email_content)
        if match_subj:
            subject = match_subj.group(1).strip()

        # 3. Build an LLM prompt for deeper extraction
        prompt = f"""
        Extract from email:
        - Intent details
        - Urgency level [Low/Medium/High]
        - Key entities
        Email: {email_content[:10000]}
        {context_str}
        """
        response = self.model.generate_content(prompt)

        # 4. Store extracted fields (sender, subject, urgency, LLM details)
        extracted = {
            "sender": sender,
            "subject": subject,
            "urgency": "Medium",           # default or could refine via LLM
            "details": response.text
        }
        self.memory.update_entry(conv_id, extracted_fields=extracted)
        return extracted
