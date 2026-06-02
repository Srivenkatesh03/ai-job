import json
from typing import Any, AsyncGenerator, Dict, List, Optional, Type
import httpx
from pydantic import BaseModel

from app.ai.providers.base_provider import AIResponse, BaseProvider


class OllamaProvider(BaseProvider):
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        default_model: str = "llama3",
    ):
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
        """Call local Ollama Chat completion API."""
        model_name = model or self.default_model
        url = f"{self.base_url}/api/chat"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload: Dict[str, Any] = {
            "model": model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
            }
        }
        
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        # Handle structured outputs
        if schema:
            payload["format"] = "json"
            schema_json = json.dumps(schema.model_json_schema())
            messages[-1]["content"] += (
                f"\n\nResponse must strictly follow this JSON schema. Return ONLY valid JSON and nothing else:\n{schema_json}"
            )

        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            res_data = response.json()
            
            content = res_data["message"]["content"] or ""
            
            # Ollama doesn't return exact token counts in API the same way, but it does return
            # prompt_eval_count (prompt tokens) and eval_count (completion tokens)
            prompt_tokens = res_data.get("prompt_eval_count", 0)
            completion_tokens = res_data.get("eval_count", 0)

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
        """Stream chunks from local Ollama API."""
        model_name = model or self.default_model
        url = f"{self.base_url}/api/chat"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model_name,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": temperature,
            }
        }
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        async with httpx.AsyncClient(timeout=90.0) as client:
            async with client.stream("POST", url, json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    try:
                        chunk = json.loads(line)
                        delta = chunk.get("message", {}).get("content", "")
                        if delta:
                            yield delta
                    except json.JSONDecodeError:
                        continue

    async def embed(
        self,
        texts: List[str],
        **kwargs: Any,
    ) -> List[List[float]]:
        """Generate local embeddings using Ollama embedding API."""
        url = f"{self.base_url}/api/embeddings"
        model_name = kwargs.get("model") or self.default_model
        
        embeddings = []
        async with httpx.AsyncClient(timeout=60.0) as client:
            for text in texts:
                payload = {
                    "model": model_name,
                    "prompt": text,
                }
                response = await client.post(url, json=payload)
                response.raise_for_status()
                res_data = response.json()
                embeddings.append(res_data["embedding"])
        return embeddings

    async def health_check(self) -> bool:
        """Check if local Ollama service is up and running."""
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.get(self.base_url)
                # Ollama returns "Ollama is running" on root URL
                return response.status_code == 200
        except Exception:
            return False
