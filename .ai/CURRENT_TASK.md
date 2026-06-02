# CURRENT_TASK.md

## Current Goal

Implement Phase 3 — AI Layer & Provider Abstraction.

---

## Scope

* Create AI provider folder structure `backend/app/ai/providers/`
* Implement `base_provider.py` defining the provider interface:
  * `generate()`
  * `stream()`
  * `embed()`
  * `health_check()`
* Implement `openai_provider.py` supporting standard generation, embeddings, and schema-structured JSON outputs.
* Implement `anthropic_provider.py` for Claude model generation.
* Implement `gemini_provider.py` for Google Gemini models.
* Implement `ollama_provider.py` for local model interactions.
* Implement `provider_factory.py` to seamlessly orchestrate fallback logic and provider instantiation.
* Implement prompt templates helper.
* Integrate into API routes/services.

---

## Relevant Files

```plaintext
backend/app/ai/providers/base_provider.py
backend/app/ai/providers/openai_provider.py
backend/app/ai/providers/anthropic_provider.py
backend/app/ai/providers/gemini_provider.py
backend/app/ai/providers/ollama_provider.py
backend/app/ai/providers/provider_factory.py
```

---

## Constraints

* async-first architecture
* follow base provider interface
* robust error handling, retries, and fallback logging
* prevent API key leaks
