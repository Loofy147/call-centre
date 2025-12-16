
import pytest
from src.orchestrator import AlgerianAgentOrchestrator
from src.models import IntentType

@pytest.mark.asyncio
async def test_process_message():
    tenant_config = {'tenant_id': 'test'}
    agent = AlgerianAgentOrchestrator(tenant_config)

    response = await agent.process_message(
        message="I want to make a reservation",
        customer_id="123",
        tenant_id="test"
    )

    assert response['intent'] == IntentType.RESERVATION.value
    assert response['response'] == "When would you like to book?"
