
import re
from typing import Dict, List
from src.models import Entity, Intent

class EntityExtractor:
    """Extracts entities from text (dates, times, phones, etc.)"""

    PATTERNS = {
        'phone': r'0[567]\d{8}',
        'date': r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
        'time': r'\d{1,2}[:.]\d{2}',
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    }

    def extract(self, text: str, intent: Intent) -> Dict[str, List[Entity]]:
        entities = {}
        for entity_type, pattern in self.PATTERNS.items():
            matches = [
                Entity(type=entity_type, value=match.group(0), raw_text=match.group(0), confidence=0.8)
                for match in re.finditer(pattern, text, re.IGNORECASE)
            ]
            if matches:
                entities[entity_type] = matches
        return entities
