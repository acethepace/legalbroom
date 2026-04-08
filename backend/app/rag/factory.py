import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.language_models.chat_models import BaseChatModel

class LLMFactory:
    @staticmethod
    def get_model(provider: Optional[str] = None) -> BaseChatModel:
        """
        Returns a ChatModel based on the provider.
        Default provider is determined by LLM_PROVIDER environment variable.
        """
        if provider is None:
            provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        
        if provider == "openai":
            return ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0
            )
        elif provider == "ollama":
            ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
            return ChatOllama(
                base_url=ollama_url,
                model="llama3:8b",
                temperature=0
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
