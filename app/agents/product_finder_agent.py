import dspy
from typing import List, Dict, Any
from app.agents.base_agent import BaseAgent
from app.services.product_service import ProductService

class ProductSearch(dspy.Signature):
    """Search for products and provide recommendations"""
    user_query = dspy.InputField(desc="The user's product search query")
    products = dspy.InputField(desc="List of relevant products found")
    response = dspy.OutputField(desc="A helpful response with product recommendations")

class ProductFinderAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.search = dspy.ChainOfThought(ProductSearch)
        self.product_service = ProductService()
    
    async def process(self, query: str) -> str:
        """Process product search queries"""
        try:
            # Search for products
            products = await self.product_service.search_products(query, limit=5)
            
            # Format products for the LLM
            products_text = self._format_products(products)
            
            # Generate response
            result = self.search(user_query=query, products=products_text)
            return result.response
            
        except Exception as e:
            return f"I apologize, but I encountered an error while searching for products: {str(e)}"
    
    def _format_products(self, products: List[Dict[str, Any]]) -> str:
        """Format products for LLM input"""
        if not products:
            return "No products found matching your query."
        
        formatted = []
        for product in products:
            formatted.append(
                f"- {product.get('name', 'Unknown')} "
                f"(${product.get('price', 'N/A')}) - "
                f"{product.get('description', 'No description')}"
            )
        
        return "\n".join(formatted)
