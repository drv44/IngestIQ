import redis
import time
import os
import json
from dotenv import load_dotenv

load_dotenv()

class RedisClient:
    def __init__(self):
        self.client = redis.Redis.from_url(
            os.getenv("REDIS_URL", "redis://localhost:6379"),
            decode_responses=True
        )
    
    def store(self, key: str, data: dict):
        """Store data as a Redis hash"""
        # Convert dict to string values for Redis
        redis_data = {}
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                redis_data[k] = json.dumps(v)
            else:
                redis_data[k] = str(v)
        self.client.hset(key, mapping=redis_data)
    
    def retrieve(self, key: str) -> dict:
        """Retrieve data from Redis hash"""
        data = self.client.hgetall(key)
        if not data:
            return None
        
        # Attempt to parse JSON fields
        for k, v in data.items():
            try:
                data[k] = json.loads(v)
            except json.JSONDecodeError:
                pass  # Keep as string if not JSON
        
        return data
    
    def create_conversation_id(self, source: str) -> str:
        """Generate unique conversation ID"""
        timestamp = int(time.time())
        source_hash = abs(hash(source)) % (10 ** 8)
        return f"conv_{source_hash}_{timestamp}"