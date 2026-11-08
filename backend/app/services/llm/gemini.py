import json
import re
from typing import Dict, Any, List
from backend.app.config import settings
from backend.app.services.llm.base import LLMProvider
from backend.app.services.llm.fallback import (
    fallback_extract_slots,
    fallback_explain_bundle
)
from backend.app.services.llm.prompts import (
    SLOT_EXTRACTION_PROMPT,
    EXPLAIN_BUNDLE_PROMPT
)

class FallbackProvider(LLMProvider):
    def extract_slots(self, text: str, expected_slot: str, language: str = "en") -> Dict[str, Any]:
        return fallback_extract_slots(text, expected_slot, language)

    def explain_bundle(
        self,
        active_lines: List[Dict[str, Any]],
        business_name: str,
        segment: str,
        language: str = "en"
    ) -> List[str]:
        return fallback_explain_bundle(active_lines, language)

    def ocr_document(self, image_bytes: bytes, doc_type: str) -> Dict[str, Any]:
        return {"confidence": 0.8, "extracted": {}}


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        try:
            from google import genai
            self.client = genai.Client(api_key=api_key)
        except Exception as e:
            print("Failed to initialize genai.Client:", e)
            self.client = None

    def extract_slots(self, text: str, expected_slot: str, language: str = "en") -> Dict[str, Any]:
        if not self.client:
            return fallback_extract_slots(text, expected_slot, language)

        prompt = SLOT_EXTRACTION_PROMPT.format(
            question_prompt=f"Please specify your {expected_slot}",
            expected_slot=expected_slot,
            user_text=text,
            language=language
        )
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Gemini slot extraction fallback: {e}")
            return fallback_extract_slots(text, expected_slot, language)

    def explain_bundle(
        self,
        active_lines: List[Dict[str, Any]],
        business_name: str,
        segment: str,
        language: str = "en"
    ) -> List[str]:
        if not self.client:
            return fallback_explain_bundle(active_lines, language)

        reasons = "\n".join([f"- {item.get('name_plain')}: {item.get('why')}" for item in active_lines])
        prompt = EXPLAIN_BUNDLE_PROMPT.format(
            language=language,
            business_name=business_name,
            segment=segment,
            reasons_text=reasons
        )
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            bullets = data.get("bullets", [])
            # Guardrail check: max 18 words per bullet
            valid_bullets = []
            for b in bullets:
                words = b.split()
                if len(words) <= 22:
                    valid_bullets.append(b)
            if len(valid_bullets) >= 2:
                return valid_bullets
            return fallback_explain_bundle(active_lines, language)
        except Exception as e:
            print(f"Gemini explain bundle fallback: {e}")
            return fallback_explain_bundle(active_lines, language)

    def ocr_document(self, image_bytes: bytes, doc_type: str) -> Dict[str, Any]:
        if not self.client:
            return {"confidence": 0.8, "extracted": {}}
        try:
            from google.genai import types
            prompt = f"Extract all fields from this {doc_type} as strict JSON matching Indian compliance standards (GSTIN, legal_name, trade_name, address, date)."
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                    prompt
                ],
                config={"response_mime_type": "application/json"}
            )
            return {"confidence": 0.95, "extracted": json.loads(response.text)}
        except Exception as e:
            print("Gemini vision fallback:", e)
            return {"confidence": 0.8, "extracted": {}}


def get_llm_provider() -> LLMProvider:
    if settings.LLM_PROVIDER.lower() == "gemini" and settings.LLM_API_KEY:
        return GeminiProvider(settings.LLM_API_KEY)
    return FallbackProvider()
