import json
from typing import Any, AsyncGenerator, Dict, List, Optional, Type
import httpx
from pydantic import BaseModel

from app.ai.providers.base_provider import AIResponse, BaseProvider
from app.core.config import settings


class AnthropicProvider(BaseProvider):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.anthropic.com/v1",
        default_model: str = "claude-3-5-sonnet-20241022",
    ):
        self.api_key = api_key or getattr(settings, "CLAUDE_API_KEY", None)
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
        """Call Anthropic Messages API."""
        model_name = model or self.default_model
        url = f"{self.base_url}/messages"
        
        headers = {
            "x-api-key": self.api_key or "",
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        # Handle formatting instructions if schema is required
        if schema:
            schema_json = json.dumps(schema.model_json_schema())
            schema_instruction = (
                f"\n\nResponse must strictly follow this JSON schema. Return ONLY valid JSON and nothing else:\n{schema_json}"
            )
            prompt = prompt + schema_instruction

        payload: Dict[str, Any] = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens or 1024,
        }
        
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            res_data = response.json()
            
            content = "".join([part["text"] for part in res_data["content"] if part["type"] == "text"])
            usage = res_data.get("usage", {})
            prompt_tokens = usage.get("input_tokens", 0)
            completion_tokens = usage.get("output_tokens", 0)

            return AIResponse(
                content=content,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
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
        """Stream chunks from Anthropic Messages API."""
        model_name = model or self.default_model
        url = f"{self.base_url}/messages"
        
        headers = {
            "x-api-key": self.api_key or "",
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens or 1024,
            "stream": True,
        }
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", url, headers=headers, json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        try:
                            event = json.loads(data_str)
                            event_type = event.get("type")
                            if event_type == "content_block_delta":
                                delta = event.get("delta", {})
                                if delta.get("type") == "text_delta":
                                    yield delta.get("text", "")
                        except json.JSONDecodeError:
                            continue

    async def embed(
        self,
        texts: List[str],
        **kwargs: Any,
    ) -> List[List[float]]:
        """Anthropic does not offer text embedding models natively. Fall back to OpenAI embedding."""
        import logging
        logger = logging.getLogger("ai_providers")
        logger.warning("Anthropic provider does not support text embeddings natively. Falling back to OpenAI text-embedding-3-small.")
        
        from app.ai.providers.openai_provider import OpenAIProvider
        openai = OpenAIProvider()
        return await openai.embed(texts, **kwargs)

    async def health_check(self) -> bool:
        """Verify Claude API credentials."""
        if not self.api_key or "placeholder" in self.api_key:
            return False
        try:
            await self.generate(
                prompt="ping",
                max_tokens=1,
                temperature=0.0,
            )
            return True
        except Exception:
            return False
