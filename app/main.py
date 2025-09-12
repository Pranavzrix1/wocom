from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import asyncio
from contextlib import asynccontextmanager

from app.config import settings
from app.api import products, chat
from app.services.product_service import ProductService
from app.services.elasticsearch_service import ElasticsearchService

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    
    # Initialize services
    es_service = ElasticsearchService()
    product_service = ProductService()
    
    # Wait for Elasticsearch to be ready
    await asyncio.sleep(10)
    
    # Create index and fetch products
    await es_service.create_product_index()
    await product_service.fetch_and_index_products()
    
    yield
    
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title="AI Product Search",
    description="AI-powered product search with intent detection",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
