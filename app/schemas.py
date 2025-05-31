from pydantic import BaseModel
from typing import Dict, Any, Optional

class ClassificationResult(BaseModel):
    format: str
    intent: str
    conversation_id: str

class MemoryEntry(BaseModel):
    conversation_id: str
    source: str
    format: str
    intent: str
    timestamp: str
    last_updated: Optional[str] = None
    extracted_fields: Dict[str, Any] = {}
    sender: Optional[str] = None