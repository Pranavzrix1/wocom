from fastapi import APIRouter
from pydantic import BaseModel
from app.services.intent_service import IntentService
from app.agents.product_finder_agent import ProductFinderAgent
from app.agents.general_agent import GeneralAgent
 
class ChatRequest(BaseModel):
    message: str
 
router = APIRouter()
 
@router.post("/")
async def chat_endpoint(request: ChatRequest):
    # Use the existing IntentService
    intent_service = IntentService()
    intent = await intent_service.classify_intent(request.message)
    
    # Route to appropriate agent
    if intent == "product_finder":
        # Handle product queries
        from app.services.product_service import ProductService
        product_service = ProductService()
        products = await product_service.search_products(request.message, limit=5)
        
        if products:
            product_list = "\n".join([
                f"• {p['name']} - ${p['price']}"
                for p in products
            ])
            response = f"Here are the products I found:\n\n{product_list}"
        else:
            response = "I couldn't find any products matching your request."
            
    else:
        # Handle general queries
        response = "I'm a product search assistant. Try asking about shirts, hats, or other products!"
    
    return {
        "response": response,
        "intent": intent
    }