
import pytest
from src.classifiers import AlgerianLanguageDetector, IntentClassifier
from src.models import Language, IntentType

def test_language_detection():
    detector = AlgerianLanguageDetector()

    # Test Darija detection
    result = detector.detect("نحب ندير réservation غدوة")
    assert result.primary == Language.MIXED
    assert result.contains_darija == True
    assert result.contains_french == True

    # Test French detection
    result = detector.detect("je veux une réservation")
    assert result.primary == Language.FRENCH

def test_intent_classification():
    classifier = IntentClassifier()

    # Test reservation intent
    intent = classifier.classify("نحب نحجز طاولة غدوة")
    assert intent.type == IntentType.RESERVATION
    assert intent.confidence > 0.2

    # Test inquiry intent
    intent = classifier.classify("what is the price?")
    assert intent.type == IntentType.INQUIRY

    # Test toxic intent
    intent = classifier.classify("you are a dog")
    assert intent.type == IntentType.TOXIC
