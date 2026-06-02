import json
from typing import Any, AsyncGenerator, Dict, List, Optional, Type
import httpx
from pydantic import BaseModel

from app.ai.providers.base_provider import AIResponse, BaseProvider
from app.core.config import settings


class OpenAIProvider(BaseProvider):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.openai.com/v1",
        default_model: str = "gpt-4o-mini",
    ):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.base_url = base_url
        self.default_model = default_model

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        schema: Optional[Type[BaseModel]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        model: Optional[str] = None,
        **kwargs: Any,
    ) -> AIResponse:
        """Call OpenAI chat completion API."""
        model_name = model or self.default_model
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload: Dict[str, Any] = {
            "model": model_name,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens

        # Handle structured outputs
        if schema:
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": schema.__name__,
                    "strict": True,
                    "schema": schema.model_json_schema(),
                }
            }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            res_data = response.json()
            
            choice = res_data["choices"][0]
            content = choice["message"]["content"] or ""
            usage = res_data.get("usage", {})
            
            return AIResponse(
                content=content,
                prompt_tokens=usage.get("prompt_tokens", 0),
                completion_tokens=usage.get("completion_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
                raw=res_data,
            )

    async def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        model: Optional[str] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[str, None]:
        """Stream chunks from OpenAI chat completion."""
        model_name = model or self.default_model
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model_name,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", url, headers=headers, json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_str)
                            delta = chunk["choices"][0]["delta"]
                            if "content" in delta and delta["content"]:
                                yield delta["content"]
                        except (json.JSONDecodeError, KeyError):
                            continue

    async def embed(
        self,
        texts: List[str],
        model: str = "text-embedding-3-small",
        **kwargs: Any,
    ) -> List[List[float]]:
        """Generate high-dimensional vector embeddings."""
        url = f"{self.base_url}/embeddings"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "input": texts,
            "model": model,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            res_data = response.json()
            return [item["embedding"] for item in res_data["data"]]

    async def health_check(self) -> bool:
        """Verify API key and status check."""
        if not self.api_key or "placeholder" in self.api_key:
            return False
        try:
            # Low token request to check credentials
            await self.generate(
                prompt="ping",
                max_tokens=1,
                temperature=0.0,
            )
            return True
        except Exception:
            return False
