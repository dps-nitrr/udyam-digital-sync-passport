import re
from typing import Dict, Any, Optional

HINDI_NUMBER_WORDS = {
    "ek": 1, "aik": 1, "single": 1, "one": 1,
    "do": 2, "doh": 2, "two": 2,
    "teen": 3, "tin": 3, "three": 3,
    "char": 4, "chaar": 4, "four": 4,
    "paanch": 5, "panch": 5, "five": 5,
    "chhe": 6, "che": 6, "six": 6,
    "saat": 7, "seven": 7,
    "aath": 8, "eight": 8,
    "nau": 9, "nine": 9,
    "das": 10, "ten": 10,
    "pandrah": 15, "fifteen": 15,
    "bees": 20, "twenty": 20,
    "pachees": 25, "twenty five": 25,
    "pachaas": 50, "fifty": 50,
    "sau": 100, "hundred": 100
}

SPECIALIST_KEYWORDS = [
    "talk to someone", "human", "specialist", "agent", "call me", "representative",
    "kisi se baat", "baat karni hai", "customer care", "help desk", "executive", "support"
]

def check_specialist_handoff(text: str) -> bool:
    clean = text.lower().strip()
    return any(kw in clean for kw in SPECIALIST_KEYWORDS)

def parse_number_from_text(text: str) -> Optional[int]:
    clean = text.lower().strip()
    
    # 1. Look for digits
    digit_match = re.search(r"\b(\d+)\b", clean)
    if digit_match:
        return int(digit_match.group(1))
        
    # 2. Look for word matches
    words = re.findall(r"\w+", clean)
    for w in words:
        if w in HINDI_NUMBER_WORDS:
            return HINDI_NUMBER_WORDS[w]
            
    return None

def parse_spend_from_text(text: str) -> Optional[float]:
    clean = text.lower().replace(",", "").strip()
    
    # Look for '2k', '3.5k'
    k_match = re.search(r"(\d+(?:\.\d+)?)\s*k\b", clean)
    if k_match:
        return float(k_match.group(1)) * 1000

    # Look for currency symbols or numbers
    amt_match = re.search(r"(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)", clean)
    if amt_match:
        val = float(amt_match.group(1))
        if val > 50:  # reasonable spend
            return val
            
    # Check words like 'teen hazar', 'paanch hazar'
    for w, num in HINDI_NUMBER_WORDS.items():
        if f"{w} hazar" in clean or f"{w} thousand" in clean:
            return float(num * 1000)

    return None

def fallback_extract_slots(text: str, expected_slot: str, language: str = "en") -> Dict[str, Any]:
    wants_specialist = check_specialist_handoff(text)
    if wants_specialist:
        return {
            "slot_name": expected_slot,
            "value": None,
            "confidence": 1.0,
            "wants_specialist": True
        }

    val = None
    confidence = 0.5

    if expected_slot in ["sites", "employees"]:
        num = parse_number_from_text(text)
        if num is not None:
            val = max(1, num)
            confidence = 0.95
    elif expected_slot in ["current_spend", "spend"]:
        spend = parse_spend_from_text(text)
        if spend is not None:
            val = spend
            confidence = 0.90
    elif expected_slot == "pain_point":
        clean = text.lower()
        if any(w in clean for w in ["speed", "slow", "dheema", "slow internet"]):
            val = "Slow internet speed"
            confidence = 0.90
        elif any(w in clean for w in ["down", "cut", "disconnect", "band", "drops", "downtime"]):
            val = "Frequent connection drops"
            confidence = 0.90
        elif any(w in clean for w in ["cost", "expensive", "bill", "mehanga", "high price"]):
            val = "High telecom expenses"
            confidence = 0.90
        elif any(w in clean for w in ["security", "hack", "virus", "cctv", "camera"]):
            val = "Security & surveillance needs"
            confidence = 0.90
        else:
            val = text.strip()[:40]
            confidence = 0.70

    return {
        "slot_name": expected_slot,
        "value": val,
        "confidence": confidence,
        "wants_specialist": False
    }

def fallback_explain_bundle(active_lines: list, language: str = "en") -> list:
    """
    Produces deterministic 3-bullet explanation under 18 words each.
    """
    bullets = []
    if language == "hi":
        for item in active_lines[:3]:
            why = item.get("why", "")
            bullets.append(f"• {item.get('name_plain', 'प्रोडक्ट')}: {why[:70]}")
        while len(bullets) < 3:
            bullets.append("• गारंटीड 99.5% अपटाइम और चौबीसों घंटे व्यापारिक तकनीकी सहायता।")
    else:
        for item in active_lines[:3]:
            why = item.get("why", "")
            bullets.append(f"• {item.get('name_plain', 'Service')}: {why[:70]}")
        while len(bullets) < 3:
            bullets.append("• 99.5% guaranteed network uptime with round-the-clock priority enterprise support.")

    return bullets[:3]
