
import pytest
from src.classifiers import AlgerianLanguageDetector
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
