import re
import json
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)

def extract_email_metadata(content: str) -> dict:
    """Extract basic email metadata using regex"""
    sender = re.search(r'From:\s*(.+?)\n', content)
    subject = re.search(r'Subject:\s*(.+?)\n', content)
    date = re.search(r'Date:\s*(.+?)\n', content)
    
    return {
        "sender": sender.group(1).strip() if sender else "Unknown",
        "subject": subject.group(1).strip() if subject else "",
        "date": date.group(1).strip() if date else ""
    }

def safe_json_parse(data: str) -> dict:
    """Safely parse JSON with fallback"""
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        # Attempt to fix common JSON issues
        try:
            # Try fixing trailing commas
            fixed = re.sub(r',\s*}', '}', re.sub(r',\s*]', ']', data))
            return json.loads(fixed)
        except:
            return {"error": "Invalid JSON", "original": data}