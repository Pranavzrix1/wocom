from fastapi import APIRouter
from pydantic import BaseModel
from app.services.intent_handler import IntentHandler

from app.agents.product_finder_agent import ProductFinderAgent
from app.agents.general_agent import GeneralAgent
from app.agents.category_finder_agent import CategoryFinderAgent

# from app.agents.product_finder_agent import ProductFinderAgent  # ← ADD THIS

 
class ChatRequest(BaseModel):
    message: str
 
router = APIRouter()

intent_service = IntentHandler()
general_agent = GeneralAgent()
category_agent = CategoryFinderAgent()


@router.post("/")
async def chat_endpoint(request: ChatRequest):
    
    # intent, confidence = await intent_service.classify_intent(request.message)
    intent, confidence = intent_service.classify_intent(request.message)

    # if intent == "product_finder":
    #     from app.services.product_service import ProductService
    #     product_service = ProductService()
    #     products = await product_service.search_products(request.message, limit=5)
        
    #     if products:
    #         product_list = "\n".join([
    #             f"• {p['name']} - ${p['price']}"
    #             for p in products
    #         ])
    #         response = f"Here are the products I found:\n\n{product_list}"
    #     else:
    #         response = "I couldn't find any products matching your request."



    if intent == "product_finder":
        product_agent = ProductFinderAgent()  # Use the intelligent agent
        response = await product_agent.process(request.message)

    elif intent == "category_finder":  # ← ADD THIS
        response = await category_agent.process(request.message)

    else:
        # Use LLM for general queries

        response = await general_agent.process(request.message)
    
    return {
        "response": response,
        "intent": intent,
        "confidence": confidence
    }