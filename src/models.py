
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any
from datetime import datetime

class Language(Enum):
    DARIJA = "darija"
    FRENCH = "french"
    MSA = "msa"
    MIXED = "mixed"

class IntentType(Enum):
    RESERVATION = "reservation"
    INQUIRY = "inquiry"
    COMPLAINT = "complaint"
    TECHNICAL_SUPPORT = "technical_support"
    BILLING = "billing"
    CANCEL_REQUEST = "cancel_request"
    STATUS_CHECK = "status_check"
    TOXIC = "toxic"

@dataclass
class LanguageContext:
    primary: Language
    contains_darija: bool = False
    contains_french: bool = False
    contains_msa: bool = False
    darija_words: List[str] = field(default_factory=list)
    french_words: List[str] = field(default_factory=list)
    confidence: float = 0.0

@dataclass
class Entity:
    type: str
    value: str
    raw_text: str
    confidence: float

@dataclass
class Intent:
    type: IntentType
    confidence: float
    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConversationContext:
    conversation_id: str
    tenant_id: str
    customer_id: str
    language_context: LanguageContext
    intent_history: List[Intent] = field(default_factory=list)
    entities: Dict[str, List[Entity]] = field(default_factory=dict)
    pending_reservation: Optional[Dict] = None
    conversation_history: List[Dict] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
