from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:password@postgres:5432/aiproducts"
    redis_url: str = "redis://redis:6379"
    elasticsearch_url: str = "http://elasticsearch:9200"
    ollama_url: str = "http://ollama:11434"
    # gemini_api_key: str = "AIzaSyClTVTxyvOfo1AxlIkrXkMj7apIUvPRr78"
    openai_api_key: str = "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"
    product_endpoint: str = "https://newscnbnc.webserver9.com/wp-json/mcp/v1/rpc"
    
    class Config:
        env_file = ".env"

settings = Settings()




# AIzaSyClTVTxyvOfo1AxlIkrXkMj7apIUvPRr78
# AIzaSyCsKJhgTOdQ72syjuBmOpjqE3w4Rmy99lE