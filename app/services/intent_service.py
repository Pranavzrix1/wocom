import dspy
from typing import Literal
from app.config import settings

class IntentClassifier(dspy.Signature):
    """Classify user intent as either general or product_finder"""
    user_query = dspy.InputField(desc="The user's query or message")
    intent = dspy.OutputField(desc="Either 'general' or 'product_finder'")

class IntentService:
    def __init__(self):
        # Configure DSPy with Gemini
        self.lm = dspy.Google(
            model="gemini-1.5-flash",
            api_key=settings.gemini_api_key
        )
        dspy.settings.configure(lm=self.lm)
        
        self.classifier = dspy.Predict(IntentClassifier)
    
    async def classify_intent(self, user_query: str) -> Literal["general", "product_finder"]:
        """Classify user intent using DSPy and Gemini"""
        try:
            result = self.classifier(user_query=user_query)
            intent = result.intent.lower().strip()
            
            if intent in ["general", "product_finder"]:
                return intent
            else:
                # Default to general if unclear
                return "general"
                
        except Exception as e:
            print(f"Intent classification error: {e}")
            return "general"
