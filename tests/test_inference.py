
import pytest
from src.inference import normalize_text

def test_normalize_text_english():
    """Tests normalization of standard English text."""
    input_text = "Hello, World! This is a test."
    expected_output = "helo world this is a test"
    assert normalize_text(input_text) == expected_output

def test_normalize_text_arabic():
    """Tests normalization of Arabic text with diacritics and special characters."""
    input_text = "مَرْحَبًا بِالعَالَمِ، هَذَا اختبار."
    expected_output = "مرحبا بالعالم هذا اختبار"
    assert normalize_text(input_text) == expected_output

def test_normalize_text_arabic_char_variations():
    """Tests normalization of different forms of Arabic characters."""
    input_text = "مرحباً بالعالم، هذا إختبار آخر."
    expected_output = "مرحبا بالعالم هذا اختبار اخر"
    assert normalize_text(input_text) == expected_output

def test_normalize_text_with_repeated_chars():
    """Tests normalization of text with repeated characters."""
    input_text = "Hellooo Wooorld"
    expected_output = "helo world"
    assert normalize_text(input_text) == expected_output

def test_normalize_text_empty_string():
    """Tests normalization of an empty string."""
    input_text = ""
    expected_output = ""
    assert normalize_text(input_text) == expected_output

def test_normalize_text_with_only_punctuation():
    """Tests normalization of a string with only punctuation."""
    input_text = ".,!?"
    expected_output = ""
    assert normalize_text(input_text) == expected_output

def test_normalize_text_with_mixed_languages():
    """Tests normalization of mixed English and Arabic text."""
    input_text = "Hello مرحباً"
    expected_output = "helo مرحبا"
    assert normalize_text(input_text) == expected_output
