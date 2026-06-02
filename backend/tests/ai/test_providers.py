import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pydantic import BaseModel, Field

import httpx
from app.ai.providers import ai_factory, AIResponse
from app.ai.providers.openai_provider import OpenAIProvider
from app.ai.providers.anthropic_provider import AnthropicProvider
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.providers.ollama_provider import OllamaProvider


# Simple schema for testing structured outputs
class ProfileSummary(BaseModel):
    summary: str
    skills: list[str] = Field(default_factory=list)


@pytest.mark.asyncio
async def test_openai_provider_generate_success():
    """Test OpenAIProvider successful raw chat completion generation."""
    provider = OpenAIProvider(api_key="test_key")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Hello! I am OpenAI."
                }
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 15,
            "total_tokens": 25
        }
    }

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        response = await provider.generate(prompt="Hello", model="gpt-4o-mini")
        
        assert response.content == "Hello! I am OpenAI."
        assert response.prompt_tokens == 10
        assert response.completion_tokens == 15
        assert response.total_tokens == 25
        
        # Verify direct HTTP post parameters
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs["json"]["model"] == "gpt-4o-mini"
        assert "Authorization" in kwargs["headers"]


@pytest.mark.asyncio
async def test_openai_provider_structured_output():
    """Test OpenAIProvider parsing structured outputs correctly via Pydantic schema."""
    provider = OpenAIProvider(api_key="test_key")

    profile_data = {
        "summary": "Experienced python engineer.",
        "skills": ["Python", "FastAPI"]
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": json.dumps(profile_data)
                }
            }
        ]
    }

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        response = await provider.generate(
            prompt="summarize me",
            schema=ProfileSummary
        )
        
        # Verify content parses successfully into Pydantic schema
        parsed = ProfileSummary.model_validate_json(response.content)
        assert parsed.summary == "Experienced python engineer."
        assert "FastAPI" in parsed.skills


@pytest.mark.asyncio
async def test_anthropic_provider_generate_success():
    """Test AnthropicProvider messages payload extraction."""
    provider = AnthropicProvider(api_key="test_key")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "content": [{"type": "text", "text": "Claude is online."}],
        "usage": {
            "input_tokens": 12,
            "output_tokens": 18
        }
    }

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        response = await provider.generate(prompt="Who are you?")
        assert response.content == "Claude is online."
        assert response.prompt_tokens == 12
        assert response.completion_tokens == 18
        assert response.total_tokens == 30


@pytest.mark.asyncio
async def test_gemini_provider_generate_success():
    """Test GeminiProvider contents structure extraction."""
    provider = GeminiProvider(api_key="test_key")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": "Gemini response"}]
                }
            }
        ],
        "usageMetadata": {
            "promptTokenCount": 5,
            "candidatesTokenCount": 8,
            "totalTokenCount": 13
        }
    }

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        response = await provider.generate(prompt="Gemini check")
        assert response.content == "Gemini response"
        assert response.prompt_tokens == 5
        assert response.completion_tokens == 8


@pytest.mark.asyncio
async def test_provider_factory_failover_success():
    """Test ProviderFactory automatically falls back to secondary options on primary failure."""
    # We will trigger OpenAI failure (raise HTTPError or exception)
    # and verify it tries Anthropic next, which will succeed.

    # Mock health checks to pass
    with patch("app.ai.providers.openai_provider.OpenAIProvider.health_check", new_callable=AsyncMock) as mock_open_health, \
         patch("app.ai.providers.anthropic_provider.AnthropicProvider.health_check", new_callable=AsyncMock) as mock_anthropic_health:
        
        mock_open_health.return_value = True
        mock_anthropic_health.return_value = True

        # Mock OpenAI generate to fail with exception
        with patch("app.ai.providers.openai_provider.OpenAIProvider.generate", new_callable=AsyncMock) as mock_openai_gen, \
             patch("app.ai.providers.anthropic_provider.AnthropicProvider.generate", new_callable=AsyncMock) as mock_anth_gen:
            
            mock_openai_gen.side_effect = httpx.ConnectTimeout("Connection timed out to openai.com")
            
            # Anthropic succeeds
            mock_anth_gen.return_value = AIResponse(
                content="Fallback Claude response",
                prompt_tokens=15,
                completion_tokens=20,
                total_tokens=35
            )

            # Trigger generation with fallback orchestration
            response = await ai_factory.generate_with_fallback(
                prompt="test trigger",
                primary_provider="openai",
                fallback_providers=["anthropic", "gemini"]
            )
            
            # Verify response was resolved by Anthropic
            assert response.content == "Fallback Claude response"
            assert response.total_tokens == 35
            
            # Asserts execution path
            mock_openai_gen.assert_called_once()
            mock_anth_gen.assert_called_once()


@pytest.mark.asyncio
async def test_provider_factory_schema_validation_failover():
    """Test ProviderFactory falls back to next provider if output doesn't match Pydantic schema."""
    
    with patch("app.ai.providers.openai_provider.OpenAIProvider.health_check", new_callable=AsyncMock) as mock_open_health, \
         patch("app.ai.providers.anthropic_provider.AnthropicProvider.health_check", new_callable=AsyncMock) as mock_anthropic_health:
        
        mock_open_health.return_value = True
        mock_anthropic_health.return_value = True

        with patch("app.ai.providers.openai_provider.OpenAIProvider.generate", new_callable=AsyncMock) as mock_openai_gen, \
             patch("app.ai.providers.anthropic_provider.AnthropicProvider.generate", new_callable=AsyncMock) as mock_anth_gen:
            
            # OpenAI generates malformed JSON content that fails ProfileSummary validation
            mock_openai_gen.return_value = AIResponse(
                content="malformed plain text output, not JSON",
                prompt_tokens=10,
                completion_tokens=10
            )

            # Claude generates correct structured format
            profile_data = {
                "summary": "Valid structure.",
                "skills": ["Testing"]
            }
            mock_anth_gen.return_value = AIResponse(
                content=json.dumps(profile_data),
                prompt_tokens=10,
                completion_tokens=10
            )

            response = await ai_factory.generate_with_fallback(
                prompt="need profile",
                schema=ProfileSummary,
                primary_provider="openai",
                fallback_providers=["anthropic"]
            )

            # Assert response is resolved by Anthropic because of OpenAI schema mismatch
            assert response.content == json.dumps(profile_data)
            parsed = ProfileSummary.model_validate_json(response.content)
            assert parsed.summary == "Valid structure."
            
            # Asserts both tried
            mock_openai_gen.assert_called_once()
            mock_anth_gen.assert_called_once()


@pytest.mark.asyncio
async def test_prompt_manager_loading_and_rendering():
    """Test that PromptManager correctly parses YAML templates and interpolates arguments."""
    from app.ai.prompt_manager import prompt_manager
    
    # Verify categories exist
    assert "resume_optimization" in prompt_manager._templates
    assert "cover_letter" in prompt_manager._templates

    # Test raw retrieval
    raw_system = prompt_manager.get_template("resume_optimization", "system")
    assert "ATS" in raw_system

    # Test dynamic interpolation
    rendered_user = prompt_manager.render_prompt(
        category="cover_letter",
        template_type="user",
        company="Google",
        role="AI Engineer",
        job_description="Build advanced AI pipelines.",
        resume_text="Senior python engineer with 5 years experience."
    )
    
    assert "Company: Google" in rendered_user
    assert "Role: AI Engineer" in rendered_user
    assert "Build advanced AI pipelines." in rendered_user


@pytest.mark.asyncio
async def test_anthropic_provider_embedding_fallback():
    """Test AnthropicProvider.embed delegates to OpenAIProvider.embed on call."""
    provider = AnthropicProvider(api_key="claude_key")
    
    mock_embeddings = [[0.1, 0.2, 0.3]]

    with patch("app.ai.providers.openai_provider.OpenAIProvider.embed", new_callable=AsyncMock) as mock_openai_embed:
        mock_openai_embed.return_value = mock_embeddings
        
        result = await provider.embed(texts=["test embedding fallback"])
        
        # Verify fallback delegation succeeded
        assert result == mock_embeddings
        mock_openai_embed.assert_called_once_with(["test embedding fallback"])
