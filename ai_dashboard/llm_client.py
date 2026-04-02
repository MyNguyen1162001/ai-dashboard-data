"""
LLM client for OpenRouter API integration.
"""
import json
import os
import re
from typing import Dict, Any
import requests
from prompts import get_schema_analysis_prompt, get_narrative_prompt


class LLMClient:
    """Interface to OpenRouter API for schema analysis and narrative generation."""

    def __init__(self, api_key: str = None, model: str = "openai/gpt-4o"):
        """Initialize OpenRouter client."""
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"

    def analyze_schema(self, schema_summary: str) -> Dict[str, Any]:
        """Send schema to LLM and get chart/KPI decisions."""
        prompt = get_schema_analysis_prompt(schema_summary)

        try:
            response = self._call_api(prompt)
            result = self._parse_json(response)
            result["reasoning"] = self._extract_reasoning(response)
            return result
        except Exception as e:
            print(f"Error calling OpenRouter API: {e}")
            return self._default_schema_response()

    def generate_narrative(self, aggregated_data: str) -> Dict[str, Any]:
        """Send aggregated results to LLM and get insights."""
        prompt = get_narrative_prompt(aggregated_data)

        try:
            response = self._call_api(prompt)
            return self._parse_json(response)
        except Exception as e:
            print(f"Error calling OpenRouter API: {e}")
            return self._default_narrative_response()

    def _call_api(self, prompt: str) -> str:
        """Make API call to OpenRouter."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/tramynguyen/ai-dashboard",
            "X-Title": "AI Dashboard Generator"
        }

        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4096,
            "temperature": 0.1
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"]
        if content is None:
            raise ValueError("LLM returned null content - model may be unavailable")
        return content

    @staticmethod
    def _extract_reasoning(text: str) -> str:
        """Extract the free-form reasoning that appears before the JSON block."""
        if not text:
            return ""
        json_start = text.find("```json")
        if json_start == -1:
            json_start = text.find("{")
        return text[:json_start].strip()

    @staticmethod
    def _parse_json(text: str) -> Dict[str, Any]:
        """Extract and parse JSON from LLM response."""
        if text is None:
            return {}
        # Try to find JSON in response (may have explanatory text)
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        # Fallback: try to parse entire response
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            return {}

    @staticmethod
    def _default_schema_response() -> Dict[str, Any]:
        """Return default schema response if LLM fails."""
        return {
            "dashboard_title": "Data Dashboard",
            "kpis": [],
            "charts": [],
            "group_by": None
        }

    @staticmethod
    def _default_narrative_response() -> Dict[str, Any]:
        """Return default narrative response if LLM fails."""
        return {
            "chart_insights": [],
            "overall_summary": "Analysis complete."
        }
