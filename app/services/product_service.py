import httpx
import asyncio
from typing import List, Dict, Any
from app.config import settings
from app.services.elasticsearch_service import ElasticsearchService

class ProductService:
    def __init__(self):
        self.es_service = ElasticsearchService()
        
    async def fetch_products_from_endpoint(self) -> List[Dict[str, Any]]:
        """Fetch products from WordPress with proper data transformation"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    settings.product_endpoint,
                    json={
                        "jsonrpc": "2.0",
                        "method": "get_products",
                        "params": {},
                        "id": 1
                    },
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    raw_products = data.get("result", [])
                    
                    # Transform WordPress data to our format
                    products = []
                    for item in raw_products:
                        # Only include products with valid prices
                        price_str = item.get("price", "")
                        if not price_str or price_str == "":
                            continue
                            
                        try:
                            price = float(price_str)
                        except (ValueError, TypeError):
                            continue
                            
                        products.append({
                            "id": item.get("id"),
                            "name": item.get("name", "Unknown Product"),
                            "description": item.get("description", ""),
                            "price": price,
                            "category": ", ".join(item.get("categories", ["Uncategorized"])),
                            "sku": str(item.get("id", "")),


                            "status": item.get("status", "publish"),
                            "stock_status": item.get("stock_status", "instock"),
                            "images": item.get("images", []),  # This is the image array!
                            "image": item.get("images", [None])[0] if item.get("images") else None,  # First image URL
                        
                            "url": item.get("permalink") or (
                                f"https://newscnbnc.webserver9.com/product/{item.get('slug')}/" 
                                if item.get("slug") 
                                else f"https://newscnbnc.webserver9.com/product/{item.get('id')}/"
                            ),
                            "slug": item.get("slug", "")
                        
                        })
                    
                    
                    return products
                else:
                    print(f"Error fetching products: {response.status_code}")
                    return []
                    
            except Exception as e:
                print(f"Exception fetching products: {e}")
                return []
    
    async def fetch_and_index_products(self):
        """Fetch products and index them in Elasticsearch"""
        print("Fetching products from WordPress endpoint...")
        products = await self.fetch_products_from_endpoint()
        
        if products:
            print(f"Found {len(products)} products with valid prices")
            print(f"Indexing {len(products)} products...")
            await self.es_service.index_products(products)
            print("Products indexed successfully!")
        else:
            print("No products found to index")
    
    async def search_products(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search products using Elasticsearch with error handling"""
        try:
            return await self.es_service.search_products(query, limit)
        except Exception as e:
            print(f"Product search error: {e}")
            return []
        

    async def get_product_categories(self) -> List[Dict[str, Any]]:
        """Fetch product categories from WooCommerce endpoint"""
        async with httpx.AsyncClient() as client:
            try:
                # Call WooCommerce categories endpoint
                response = await client.post(
                    settings.product_endpoint,
                    json={
                        "jsonrpc": "2.0",  # ← ADD THIS
                        "method": "get_product_categories",
                        "params": {},
                        "id": 1  # ← ADD THIS
                    },
                    headers={"Content-Type": "application/json"}  # ← ADD THIS
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"🔍 Category Response Debug: {data}")  # ← ADD THIS DEBUG LINE
                    
                    # Try multiple response formats
                    if data.get("success"):
                        return data.get("data", [])
                    elif data.get("result"):  # ← ADD THIS (same as products)
                        return data.get("result", [])
                    elif isinstance(data, list):  # ← ADD THIS (direct array)
                        return data
                    else:
                        print(f"❌ Unexpected category response format: {data}")
                
                print(f"Categories fetch failed: {response.status_code}")
                return []
            except Exception as e:
                print(f"Error fetching categories: {e}")
                return []


    async def fetch_and_index_categories(self):
        """Fetch categories from WooCommerce and index in Elasticsearch"""
        categories = await self.get_product_categories()
        
        if categories:
            await self.es_service.index_categories(categories)
            print(f"Indexed {len(categories)} categories")
        else:
            print("No categories to index")

    async def search_categories(self, query: str = "", limit: int = 50) -> List[Dict[str, Any]]:
        """Search categories using Elasticsearch"""
        return await self.es_service.search_categories(query, limit)

