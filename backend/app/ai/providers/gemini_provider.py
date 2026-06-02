import json
from typing import Any, AsyncGenerator, Dict, List, Optional, Type
import httpx
from pydantic import BaseModel

from app.ai.providers.base_provider import AIResponse, BaseProvider
from app.core.config import settings


class GeminiProvider(BaseProvider):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://generativelanguage.googleapis.com/v1beta",
        default_model: str = "gemini-1.5-flash",
    ):
        self.api_key = api_key or getattr(settings, "GEMINI_API_KEY", None)
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
        """Call Google Gemini Generate Content API."""
        model_name = model or self.default_model
        url = f"{self.base_url}/models/{model_name}:generateContent?key={self.api_key or ''}"
        
        headers = {
            "Content-Type": "application/json",
        }

        # Build contents structure
        contents = [
            {
                "parts": [{"text": prompt}]
            }
        ]

        generation_config: Dict[str, Any] = {
            "temperature": temperature,
        }
        if max_tokens:
            generation_config["maxOutputTokens"] = max_tokens

        payload: Dict[str, Any] = {
            "contents": contents,
            "generationConfig": generation_config,
        }

        if system_prompt:
            payload["systemInstruction"] = {
                "parts": [{"text": system_prompt}]
            }

        # Handle structured outputs
        if schema:
            generation_config["responseMimeType"] = "application/json"
            # Gemini expects responseSchema in a slightly specific OpenAPI-like schema format
            # Fortunately Pydantic's model_json_schema is highly compatible.
            generation_config["responseSchema"] = schema.model_json_schema()

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            res_data = response.json()

            # Parse answer content
            candidates = res_data.get("candidates", [])
            content = ""
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                content = "".join([part.get("text", "") for part in parts])

            # Parse usage metadata
            usage = res_data.get("usageMetadata", {})
            prompt_tokens = usage.get("promptTokenCount", 0)
            completion_tokens = usage.get("candidatesTokenCount", 0)
            total_tokens = usage.get("totalTokenCount", 0)

            return AIResponse(
                content=content,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
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
        """Stream chunks from Google Gemini API."""
        model_name = model or self.default_model
        url = f"{self.base_url}/models/{model_name}:streamGenerateContent?key={self.api_key or ''}"
        
        headers = {
            "Content-Type": "application/json",
        }

        contents = [{"parts": [{"text": prompt}]}]
        generation_config = {"temperature": temperature}
        if max_tokens:
            generation_config["maxOutputTokens"] = max_tokens

        payload = {
            "contents": contents,
            "generationConfig": generation_config,
        }
        if system_prompt:
            payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", url, headers=headers, json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    try:
                        # Gemini returns SSE or chunks
                        # Clean up formatting indicators
                        if line.startswith("data: "):
                            line = line[6:]
                        chunk = json.loads(line)
                        candidates = chunk.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            text = "".join([part.get("text", "") for part in parts])
                            yield text
                    except json.JSONDecodeError:
                        continue

    async def embed(
        self,
        texts: List[str],
        model: str = "text-embedding-004",
        **kwargs: Any,
    ) -> List[List[float]]:
        """Generate text vector embeddings using Gemini model."""
        url = f"{self.base_url}/models/{model}:embedContent?key={self.api_key or ''}"
        headers = {"Content-Type": "application/json"}
        
        # Check if single or batch
        if len(texts) == 1:
            payload = {
                "model": f"models/{model}",
                "content": {"parts": [{"text": texts[0]}]}
            }
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                res_data = response.json()
                return [res_data["embedding"]["values"]]
        else:
            # Batch embedding
            batch_url = f"{self.base_url}/models/{model}:batchEmbedContents?key={self.api_key or ''}"
            requests = [
                {
                    "model": f"models/{model}",
                    "content": {"parts": [{"text": text}]}
                }
                for text in texts
            ]
            payload = {"requests": requests}
            async with httpx.AsyncClient(timeout=40.0) as client:
                response = await client.post(batch_url, headers=headers, json=payload)
                response.raise_for_status()
                res_data = response.json()
                return [item["values"] for item in res_data["embeddings"]]

    async def health_check(self) -> bool:
        """Verify Gemini API credentials."""
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
