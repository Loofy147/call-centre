
from typing import Dict, Any
from src.models import Intent, ConversationContext, LanguageContext, Language, IntentType

class ResponseGenerator:
    """Generates appropriate responses based on context"""

    def __init__(self, tenant_config: Dict):
        self.tenant_config = tenant_config

    def generate(self, intent: Intent, entities: Dict, context: ConversationContext) -> Dict[str, Any]:
        if intent.type == IntentType.TOXIC:
            return self._handle_toxic_content(context.language_context)

        handler = getattr(self, f"_handle_{intent.type.name.lower()}", self._handle_inquiry)
        return handler(intent, entities, context)

    def _handle_toxic_content(self, lang_ctx: LanguageContext) -> Dict:
        return {'text': "Please be respectful.", 'action': 'flag_for_moderation', 'end_conversation': True}

    def _handle_inquiry(self, intent: Intent, entities: Dict, context: ConversationContext) -> Dict:
        return {'text': "How can I help you?", 'action': 'provide_information', 'requires_input': True}

    def _handle_reservation(self, intent: Intent, entities: Dict, context: ConversationContext) -> Dict:
        return {'text': "When would you like to book?", 'action': 'request_reservation_details', 'requires_input': True}

    def _handle_complaint(self, intent: Intent, entities: Dict, context: ConversationContext) -> Dict:
        return {'text': "I'm sorry to hear that. Please provide more details.", 'action': 'open_complaint_ticket', 'requires_input': True}
