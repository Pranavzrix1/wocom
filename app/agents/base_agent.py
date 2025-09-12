import dspy
from abc import ABC, abstractmethod
from app.config import settings

class BaseAgent(ABC):
    def __init__(self):
        self.lm = dspy.Google(
            model="gemini-1.5-flash",
            api_key=settings.gemini_api_key
        )
        dspy.settings.configure(lm=self.lm)
    
    @abstractmethod
    async def process(self, query: str) -> str:
        pass
