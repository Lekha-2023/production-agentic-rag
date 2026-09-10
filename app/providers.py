from __future__ import annotations

import os
from typing import Protocol


class LLM(Protocol):
    def generate(self, system: str, prompt: str) -> str: ...


class DeterministicLLM:
    def generate(self, system: str, prompt: str) -> str:
        return prompt


class OpenAICompatibleLLM:
    """Optional adapter; keeps credentials outside source control."""

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is required for the hosted provider")

    def generate(self, system: str, prompt: str) -> str:
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            temperature=0,
        )
        return response.choices[0].message.content or ""
