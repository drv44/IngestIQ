# app/agents/json_agent.py
import json
from pydantic import BaseModel
from ..memory.memory_manager import MemoryManager

class TargetSchema(BaseModel):
    invoice_id: str = None
    amount: float = None
    # Add other fields as needed

class JSONAgent:
    def __init__(self, memory: MemoryManager):
        self.memory = memory
        self.required_fields = ["invoice_id", "amount", "date"]
        self.context = None
    
    def set_context(self, conv_id: str):
        self.context = self.memory.get_entry(conv_id)

    def process(self, json_data: str, conv_id: str) -> dict:
        # Use context if available
        if self.context:
            # Example: Use previous extracted fields as reference
            print(f"Processing with context: {self.context['intent']}")

        try:
            data = json.loads(json_data)
            validated = TargetSchema(**data)
            missing = [field for field in self.required_fields if getattr(validated, field) is None]
            
            # Update memory
            self.memory.update_entry(conv_id, extracted_fields=data)
            
            return {
                "status": "success",
                "missing_fields": missing,
                "data": data
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}