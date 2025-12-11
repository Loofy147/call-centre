
import pytest
from src.ml_classifier import MLIntentClassifier
from src.models import IntentType

def test_ml_intent_classification():
    classifier = MLIntentClassifier()

    # Test reservation intent
    intent = classifier.classify("I want to book a table")
    assert intent.type == IntentType.RESERVATION

    # Test inquiry intent
    intent = classifier.classify("what are your opening hours?")
    assert intent.type == IntentType.INQUIRY

    # Test toxic intent
    intent = classifier.classify("you are stupid")
    assert intent.type == IntentType.TOXIC
