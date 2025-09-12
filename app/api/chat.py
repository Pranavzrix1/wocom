from fastapi import APIRouter
from pydantic import BaseModel
from app.services.intent_service import IntentService
from app.agents.general_agent import GeneralAgent
from app.agents.product_finder_agent import ProductFinderAgent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    intent: str

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat messages with intent detection"""
    intent_service = IntentService()
    
    # Classify intent
    intent = await intent_service.classify_intent(request.message)
    
    # Route to appropriate agent
    if intent == "product_finder":
        agent = ProductFinderAgent()
    else:
        agent = GeneralAgent()
    
    response = await agent.process(request.message)
    
    return ChatResponse(response=response, intent=intent)
