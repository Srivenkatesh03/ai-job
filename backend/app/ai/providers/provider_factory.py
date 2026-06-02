import logging
from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel

from app.ai.providers.base_provider import AIResponse, BaseProvider
from app.ai.providers.openai_provider import OpenAIProvider
from app.ai.providers.anthropic_provider import AnthropicProvider
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.providers.ollama_provider import OllamaProvider

logger = logging.getLogger("ai_providers")


class ProviderFactory:
    def __init__(self):
        self._providers: Dict[str, BaseProvider] = {
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
            "gemini": GeminiProvider(),
            "ollama": OllamaProvider(),
        }

    def get_provider(self, name: str) -> BaseProvider:
        """Retrieve a registered provider instance by name.
        
        Raises:
            ValueError: If the provider name is unrecognized.
        """
        provider = self._providers.get(name.lower())
        if not provider:
            raise ValueError(
                f"Unknown AI Provider: '{name}'. Supported providers: {list(self._providers.keys())}"
            )
        return provider

    async def generate_with_fallback(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        schema: Optional[Type[BaseModel]] = None,
        primary_provider: str = "openai",
        fallback_providers: Optional[List[str]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> AIResponse:
        """Generate content with automatic fallback/failover to alternative providers.
        
        Args:
            prompt: Text user prompt.
            system_prompt: Core operational parameters/instructions.
            schema: Optional Pydantic model for structured validation.
            primary_provider: Name of the primary AI provider to request first.
            fallback_providers: Sequence of alternative providers to attempt on failure.
            temperature: Sampling temperature.
            max_tokens: Limit on token production.
            
        Returns:
            Unified AIResponse object.
            
        Raises:
            RuntimeError: If all primary and fallback providers fail to generate.
        """
        if fallback_providers is None:
            # Standard platform fallback path: OpenAI -> Anthropic -> Gemini -> Ollama
            fallback_providers = ["anthropic", "gemini", "ollama"]

        # Ensure primary provider isn't repeated in fallbacks
        fallbacks = [p for p in fallback_providers if p.lower() != primary_provider.lower()]
        providers_to_try = [primary_provider] + fallbacks

        errors: List[str] = []
        
        for provider_name in providers_to_try:
            try:
                logger.info(f"Attempting generation with provider: '{provider_name}'...")
                provider = self.get_provider(provider_name)
                
                # Check health / API Key validity (only for cloud providers if keys are standard)
                if not await provider.health_check() and provider_name != "ollama":
                    # Local Ollama might not be running but we try it; if cloud API keys are placeholders we skip early.
                    logger.warning(f"Provider '{provider_name}' health check failed. Skipping to next fallback...")
                    errors.append(f"{provider_name}: health check failed (empty or placeholder API key)")
                    continue

                response = await provider.generate(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    schema=schema,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                
                # Validation checks: if schema is expected, confirm it parses correctly
                if schema:
                    try:
                        # Attempt to parse output content to validate schema matching
                        schema.model_validate_json(response.content)
                    except Exception as parse_error:
                        logger.error(
                            f"Response validation failed for provider '{provider_name}': {parse_error}. Trying fallback..."
                        )
                        errors.append(f"{provider_name}: output schema validation failed - {str(parse_error)}")
                        continue
                
                logger.info(f"Generation successful using provider: '{provider_name}'.")
                return response

            except Exception as e:
                logger.error(f"Error occurred during generation with provider '{provider_name}': {e}")
                errors.append(f"{provider_name}: {str(e)}")
                continue

        error_summary = " | ".join(errors)
        raise RuntimeError(
            f"All configured AI Providers failed to generate. Execution trace: {error_summary}"
        )


# Global singleton instance
ai_factory = ProviderFactory()
