from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any
from app.services.product_service import ProductService
import traceback

router = APIRouter()

@router.get("/search")
async def search_products(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50)
) -> List[Dict[str, Any]]:
    """Search products with comprehensive error handling"""
    try:
        product_service = ProductService()
        results = await product_service.search_products(q, limit)
        return results
    except Exception as e:
        print(f"Search endpoint error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        # Return empty list instead of crashing
        return []

@router.post("/refresh")
async def refresh_products():
    """Refresh products from endpoint with error handling"""
    try:
        product_service = ProductService()
        await product_service.fetch_and_index_products()
        return {"message": "Products refreshed successfully"}
    except Exception as e:
        print(f"Refresh endpoint error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error refreshing products: {str(e)}")
