
from transformers import pipeline
from src.models import Intent, IntentType

class MLIntentClassifier:
    """
    ML-based intent classifier using a zero-shot classification model.
    """

    def __init__(self, model_name="MoritzLaurer/bge-m3-zeroshot-v2.0"):
        """
        Initializes the zero-shot classification pipeline.
        """
        self.classifier = pipeline("zero-shot-classification", model=model_name)
        self.intent_labels = [intent.value for intent in IntentType]

    def classify(self, text: str) -> Intent:
        """
        Classifies the intent of the given text.
        """
        hypothesis_template = "The user's message is expressing a {}."
        result = self.classifier(text, self.intent_labels, hypothesis_template=hypothesis_template, multi_label=False)

        # The top label is the predicted intent
        top_label = result['labels'][0]
        confidence = result['scores'][0]

        # Convert the label back to an IntentType enum
        intent_type = IntentType(top_label)

        return Intent(type=intent_type, confidence=confidence)
