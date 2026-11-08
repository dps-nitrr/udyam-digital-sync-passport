from abc import ABC, abstractmethod
from typing import Dict, Any, List

class LLMProvider(ABC):
    @abstractmethod
    def extract_slots(self, text: str, expected_slot: str, language: str = "en") -> Dict[str, Any]:
        """Extracts slot value from natural language or speech text."""
        pass

    @abstractmethod
    def explain_bundle(
        self,
        active_lines: List[Dict[str, Any]],
        business_name: str,
        segment: str,
        language: str = "en"
    ) -> List[str]:
        """Explains recommended bundle in 3 short bullets (max 18 words each)."""
        pass

    @abstractmethod
    def ocr_document(self, image_bytes: bytes, doc_type: str) -> Dict[str, Any]:
        """Extracts structured document JSON from image via multimodal vision."""
        pass
