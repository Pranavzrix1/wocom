# app/agents/product_finder_agent.py
from app.services.product_service import ProductService
import dspy
 
class ProductQuery(dspy.Signature):
    """Convert natural language to product search query"""
    user_query = dspy.InputField(desc="User's natural language query")
    search_terms = dspy.OutputField(desc="Optimized search terms for product search")
    response_template = dspy.OutputField(desc="How to present the results to user")
 
class ProductFinderAgent:
    def __init__(self):
        self.product_service = ProductService()
        self.query_optimizer = dspy.ChainOfThought(ProductQuery)
    
    async def process(self, user_query: str) -> str:
        # Optimize search query
        result = self.query_optimizer(user_query=user_query)
        search_terms = result.search_terms
        
        # Search products
        products = await self.product_service.search_products(search_terms, limit=5)
        
        if products:
            product_list = "\n".join([
                f"• {p['name']} - ${p['price']} ({p['category']})"
                for p in products
            ])
            return f"Yes! Here are the shirts I found:\n\n{product_list}\n\nWould you like more details about any of these?"
        else:
            return "I don't have any shirts matching your criteria right now. Could you try a different search term?"