from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List, Optional, Type
from pydantic import BaseModel, Field


class AIResponse(BaseModel):
    """Standardized wrapper for all model responses."""
    content: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    raw: Optional[Any] = None


class BaseProvider(ABC):
    """Abstract base class establishing the contract for all AI model providers."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        schema: Optional[Type[BaseModel]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> AIResponse:
        """Execute standard or structured generation against the model."""
        pass

    @abstractmethod
    async def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[str, None]:
        """Stream response chunks text as they arrive asynchronously."""
        pass

    @abstractmethod
    async def embed(
        self,
        texts: List[str],
        **kwargs: Any,
    ) -> List[List[float]]:
        """Generate high-dimensional vector embeddings for a list of string texts."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Verify API keys and connectivity with the provider host endpoint."""
        pass
