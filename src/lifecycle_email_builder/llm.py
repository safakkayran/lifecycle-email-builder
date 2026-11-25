"""LLM client with disk cache and retry logic for lifecycle-email-builder."""

from __future__ import annotations

import hashlib
import json
from typing import TYPE_CHECKING, TypeVar

from lifecycle_builder.config import get_settings
from openai import OpenAI
from pydantic import BaseModel
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

if TYPE_CHECKING:
    from pathlib import Path

T = TypeVar("T", bound=BaseModel)


class CachedLLMClient:
    """OpenAI-compatible client with disk cache and retry on 429/5xx."""

    def __init__(self, cache_dir: Path | None = None):
        settings = get_settings()
        self.client = OpenAI(
            base_url=settings.LITELLM_BASE_URL,
            api_key=settings.LITELLM_API_KEY or "not-needed",
        )
        self.cache_dir = cache_dir or settings.CACHE_DIR / "llm_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _cache_key(model: str, messages: list[dict], **kwargs) -> str:
        """Generate cache key from model and messages."""
        content = json.dumps({"model": model, "messages": messages, **kwargs}, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    def _cache_path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def _get_cached(self, key: str) -> dict | None:
        path = self._cache_path(key)
        if path.exists():
            try:
                return json.loads(path.read_text())
            except Exception:
                return None
        return None

    def _save_cache(self, key: str, response: dict) -> None:
        path = self._cache_path(key)
        path.write_text(json.dumps(response, ensure_ascii=False, indent=2))

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(Exception),
    )
    def complete(
        self,
        model: str,
        messages: list[dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4000,
        response_format: dict | None = None,
    ) -> str:
        """Call LLM with caching."""
        # Check cache (only for non-streaming, deterministic calls)
        use_cache = response_format is not None or temperature == 0
        if use_cache:
            key = self._cache_key(
                model,
                messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format,
            )
            cached = self._get_cached(key)
            if cached:
                return cached["choices"][0]["message"]["content"]

        resp = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format,
        )
        content = resp.choices[0].message.content or ""

        if use_cache:
            self._save_cache(key, resp.model_dump())

        return content

    def complete_json(self, schema: type[T], model: str, system: str, user: str, **kwargs) -> T:
        """Call LLM and parse JSON into Pydantic model with retry."""
        schema_json = schema.model_json_schema()
        response_format = {
            "type": "json_schema",
            "json_schema": {"name": schema.__name__, "schema": schema_json, "strict": True},
        }

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

        for attempt in range(3):
            try:
                content = self.complete(
                    model=model,
                    messages=messages,
                    temperature=0,
                    max_tokens=4000,
                    response_format=response_format,
                )
                return schema.model_validate_json(content)
            except Exception as e:
                if attempt == 2:
                    raise
                # Add error feedback to user message
                messages.append(
                    {"role": "assistant", "content": content if 'content' in locals() else ""}
                )
                messages.append(
                    {
                        "role": "user",
                        "content": "Previous response failed validation: "
                        f"{e}. Please fix and output valid JSON only.",
                    }
                )

        raise RuntimeError("Failed to get valid JSON after retries")


def complete_json(
    schema: type[T],
    system: str,
    user: str,
    model: str | None = None,
    **kwargs,
) -> T:
    """Convenience function for sync JSON completion."""
    settings = get_settings()
    client = CachedLLMClient()
    return client.complete_json(
        schema=schema,
        model=model or settings.LLM_MODEL,
        system=system,
        user=user,
        **kwargs,
    )