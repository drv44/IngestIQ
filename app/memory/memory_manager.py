import json
from datetime import datetime
from .redis_client import RedisClient
from ..schemas import MemoryEntry

class MemoryManager:
    def __init__(self):
        self.redis = RedisClient()
    
    def create_entry(self, source: str, format: str, intent: str) -> str:
        """Create a new conversation entry in memory"""
        conv_id = self.redis.create_conversation_id(source)
        entry = MemoryEntry(
            conversation_id=conv_id,
            source=source,
            format=format,
            intent=intent,
            timestamp=str(datetime.utcnow()),
            extracted_fields={},
            sender=None
        ).dict()
        self.redis.store(conv_id, entry)
        return conv_id
    
    def update_entry(self, conv_id: str, **updates):
        """Update an existing conversation entry"""
        existing = self.get_entry(conv_id)
        if not existing:
            raise ValueError(f"Conversation {conv_id} not found")
        
        # Merge updates with existing data
        for key, value in updates.items():
            if key == "extracted_fields" and existing.get("extracted_fields"):
                # Deep merge for extracted fields
                existing["extracted_fields"] = {
                    **existing["extracted_fields"],
                    **value
                }
            else:
                existing[key] = value
        
        # Add update timestamp
        existing["last_updated"] = str(datetime.now())
        self.redis.store(conv_id, existing)
    
    def get_entry(self, conv_id: str) -> dict:
        """Retrieve full conversation context"""
        entry = self.redis.retrieve(conv_id)
        if not entry:
            return None
        
        # Ensure extracted_fields is always a dict
        if "extracted_fields" in entry and isinstance(entry["extracted_fields"], str):
            try:
                entry["extracted_fields"] = json.loads(entry["extracted_fields"])
            except json.JSONDecodeError:
                entry["extracted_fields"] = {}
        
        return entry