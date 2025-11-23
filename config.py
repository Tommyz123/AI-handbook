"""
Configuration Management Module
Supports free/paid dual mode switching
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration class"""
    
    # Mode selection: 'free' or 'paid'
    MODE = os.getenv("MODE", "free")
    
    # OpenAI API Key (required for paid mode)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Text splitting parameters
    CHUNK_SIZE = 1500
    CHUNK_OVERLAP = 100
    
    # Retrieval parameters
    TOP_K = 3
    
    # Cache settings
    ENABLE_CACHE = True
    CACHE_DIR = "./cache"
    VECTOR_STORE_DIR = "./cache/vector_store"
    
    # Embedding model (fixed to free model)
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # LLM model configuration
    if MODE == "paid":
        LLM_MODEL = "gpt-4o-mini"
        LLM_TEMPERATURE = 0.3
    else:
        LLM_MODEL = None
        LLM_TEMPERATURE = 0.5
    
    # Prompt Template (Designed for list-based policy handbooks)
    PROMPT_TEMPLATE = """You are an experienced HR consultant who helps employees understand company policies.

Your task is to accurately answer employee questions based on the employee handbook content.

Employee Handbook Content:
{context}

Employee Question:
{question}

IMPORTANT - How to read employee handbook policies:

Employee handbooks use concise, list-based formats. When you see a policy with specific requirements or restrictions:

1. **Identify what IS explicitly stated**:
   - "Required in office: X, Y" means you MUST be in office on days X and Y
   - "Prohibited: A, B" means you CANNOT do A or B
   - "Up to N" means the MAXIMUM is N, not a requirement

2. **Understand what is NOT stated (implicit permissions)**:
   - If a policy says "Required in office: Mondays and Thursdays"
   - This explicitly requires: Monday and Thursday in office
   - This implicitly allows: Tuesday, Wednesday, Friday for other arrangements (like remote work)
   - The policy does NOT say "Only Mondays and Thursdays can be remote" - it says the OPPOSITE

3. **Combine multiple policy rules**:
   - "Required in office: Mondays and Thursdays" = Must be in office 2 days
   - "Up to 3 days per week remote work allowed" = Can work remotely up to 3 days
   - Available days for remote: Tuesday, Wednesday, Friday (5 days - 2 required = 3 available)
   - You can choose any 3 from these available days

4. **Answer the question**:
   - Match the question's language (English → English, Chinese → Chinese)
   - Be direct: "Yes" or "No" first, then explain
   - State any conditions clearly
   - Only say "not mentioned" if truly absent from the handbook

Now provide your answer:"""

    @classmethod
    def validate(cls):
        """Validate configuration"""
        if cls.MODE == "paid" and not cls.OPENAI_API_KEY:
            raise ValueError("Paid mode requires OPENAI_API_KEY environment variable")
        
        # Create necessary directories
        os.makedirs(cls.CACHE_DIR, exist_ok=True)
        os.makedirs(cls.VECTOR_STORE_DIR, exist_ok=True)
        
        return True
    
    @classmethod
    def get_config_info(cls):
        """Get configuration information"""
        return {
            "mode": cls.MODE,
            "embedding_model": cls.EMBEDDING_MODEL,
            "llm_model": cls.LLM_MODEL,
            "chunk_size": cls.CHUNK_SIZE,
            "chunk_overlap": cls.CHUNK_OVERLAP,
            "top_k": cls.TOP_K,
            "cache_enabled": cls.ENABLE_CACHE
        }


if __name__ == "__main__":
    try:
        Config.validate()
        print("✅ Configuration validated")
        print("\nCurrent configuration:")
        for key, value in Config.get_config_info().items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
