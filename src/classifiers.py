
import re
from typing import Optional
from src.models import LanguageContext, Intent, ConversationContext, Language, IntentType

class AlgerianLanguageDetector:
    """Detects language mix in Algerian conversations"""

    DARIJA_PATTERNS = {
        'نحب': 'want', 'نحوس': 'search', 'بغيت': 'want', 'واش': 'what/question',
        'كاين': 'is_there', 'شحال': 'how_much', 'بزاف': 'much/many',
    }

    FRENCH_COMMON = {
        'internet', 'connexion', 'modem', 'facture', 'carte', 'compte',
        'service', 'problème', 'rendez-vous', 'réservation', 'urgent',
    }

    def detect(self, text: str) -> LanguageContext:
        text_lower = text.lower()
        tokens = re.findall(r'\b\w+\b', text_lower)

        darija_count = sum(1 for word in self.DARIJA_PATTERNS if word in text_lower)
        french_count = sum(1 for word in self.FRENCH_COMMON if word in text_lower)

        has_arabic = bool(re.search(r'[\u0600-\u06FF]', text))

        primary = Language.MSA
        if darija_count > 0 and french_count > 0:
            primary = Language.MIXED
        elif darija_count > 0 or has_arabic:
            primary = Language.DARIJA
        elif french_count > 0:
            primary = Language.FRENCH

        return LanguageContext(
            primary=primary,
            contains_darija=darija_count > 0 or has_arabic,
            contains_french=french_count > 0,
            confidence=min((darija_count + french_count) / max(len(tokens), 1), 1.0)
        )
