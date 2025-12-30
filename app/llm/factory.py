from app.config.settings import LLM_PROVIDER, model
from app.llm.gemini_llm import GeminiLLM
from app.llm.ollama_llm import OllamaLLM

def get_llm():
    if LLM_PROVIDER == "ollama":
        return OllamaLLM()
    
    elif LLM_PROVIDER == "gemini":
        from app.llm.gemini_llm import GeminiLLM
        return GeminiLLM(model=model)
    
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")