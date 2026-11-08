from typing import Dict, Any, List, Optional, Tuple
from sqlmodel import Session
from backend.app.models import Journey
from backend.app.services.llm.gemini import get_llm_provider

QUESTIONS_CONFIG = {
    "ASK_SITES": {
        "en": "How many business locations or branches do you operate?",
        "hi": "आपके व्यवसाय के कितने स्टोर या शाखाएं (branches) हैं?",
        "slot": "sites",
        "chips": [
            {"label": "1 Store / Single Office", "value": 1},
            {"label": "2 Locations", "value": 2},
            {"label": "3 - 5 Branches", "value": 3},
            {"label": "6+ Locations", "value": 6}
        ]
    },
    "ASK_SIZE": {
        "en": "How many employees or team members work in your business?",
        "hi": "आपके व्यवसाय में लगभग कितने कर्मचारी या टीम सदस्य काम करते हैं?",
        "slot": "employees",
        "chips": [
            {"label": "1 - 4 Members", "value": 2},
            {"label": "5 - 9 Staff", "value": 6},
            {"label": "10 - 24 Team", "value": 15},
            {"label": "25+ Employees", "value": 30}
        ]
    },
    "ASK_PAIN_OR_SPEND": {
        "en": "What is your approximate current monthly telecom and internet bill?",
        "hi": "आपका वर्तमान मासिक इंटरनेट और टेलीकॉम खर्च लगभग कितना है?",
        "slot": "current_spend",
        "chips": [
            {"label": "Under ₹2,000 / mo", "value": 1800},
            {"label": "₹2,000 - ₹5,000 / mo", "value": 3500},
            {"label": "₹5,000 - ₹10,000 / mo", "value": 7500},
            {"label": "₹10,000+ / mo", "value": 12000}
        ]
    }
}

STATE_TRANSITIONS = {
    "IDENTIFY": "CONFIRM_BUSINESS",
    "CONFIRM_BUSINESS": "ASK_SITES",
    "ASK_SITES": "ASK_SIZE",
    "ASK_SIZE": "ASK_PAIN_OR_SPEND",
    "ASK_PAIN_OR_SPEND": "RECOMMEND"
}

def process_advisor_message(
    journey: Journey,
    slot: Optional[str] = None,
    chip_value: Optional[Any] = None,
    text: Optional[str] = None,
    session: Optional[Session] = None
) -> Dict[str, Any]:
    llm = get_llm_provider()
    lang = journey.language or "en"
    current_state = journey.stage or "IDENTIFY"
    slots_filled = {
        "sites": journey.sites,
        "employees": journey.employees,
        "current_spend": journey.current_spend
    }

    # Check immediate handoff request in free text
    if text:
        extracted = llm.extract_slots(text, slot or "general", lang)
        if extracted.get("wants_specialist"):
            journey.handoff = True
            journey.handoff_reason = "Customer requested to speak with a human specialist"
            if session:
                session.add(journey)
                session.commit()
            msg = "I've connected you with our dedicated solution specialist. They will call you within 15 minutes." if lang == "en" else "मैंने आपको हमारे विशेषज्ञ से जोड़ दिया है। वे आपको 15 मिनट के भीतर कॉल करेंगे।"
            return {
                "next_state": "HANDOFF",
                "assistant_message": msg,
                "chips": [],
                "slots_filled": slots_filled,
                "handoff": True,
                "handoff_reason": journey.handoff_reason,
                "llm_used": True
            }

    # Process slot value
    target_slot = slot or (QUESTIONS_CONFIG.get(current_state, {}).get("slot"))
    val = None
    if chip_value is not None:
        val = chip_value
    elif text and target_slot:
        extracted = llm.extract_slots(text, target_slot, lang)
        val = extracted.get("value")

    if val is not None and target_slot:
        if target_slot == "sites":
            journey.sites = int(val)
            slots_filled["sites"] = int(val)
            if journey.sites >= 10:
                journey.handoff = True
                journey.handoff_reason = f"Large enterprise multi-site footprint ({journey.sites} sites) routed to enterprise desk."
        elif target_slot == "employees":
            journey.employees = int(val)
            slots_filled["employees"] = int(val)
        elif target_slot in ["current_spend", "spend"]:
            journey.current_spend = float(val)
            slots_filled["current_spend"] = float(val)

    # Determine next state
    next_state = STATE_TRANSITIONS.get(current_state, "RECOMMEND")
    
    # If 10+ sites, trigger handoff
    if journey.sites >= 10:
        journey.stage = "HANDOFF"
        if session:
            session.add(journey)
            session.commit()
        return {
            "next_state": "HANDOFF",
            "assistant_message": f"Because you manage {journey.sites} sites, an Enterprise Solution Architect has been assigned to create a unified SD-WAN plan.",
            "chips": [],
            "slots_filled": slots_filled,
            "handoff": True,
            "handoff_reason": journey.handoff_reason,
            "llm_used": False
        }

    journey.stage = next_state
    if session:
        session.add(journey)
        session.commit()

    if next_state in QUESTIONS_CONFIG:
        q_conf = QUESTIONS_CONFIG[next_state]
        msg = q_conf.get(lang, q_conf["en"])
        chips = q_conf.get("chips", [])
    elif next_state == "RECOMMEND":
        msg = "We have prepared a transparent, all-inclusive monthly package tailored for your business." if lang == "en" else "हमने आपके व्यवसाय के अनुसार एक पारदर्शी मासिक पैकेज तैयार किया है।"
        chips = []
    else:
        msg = "Ready to proceed."
        chips = []

    return {
        "next_state": next_state,
        "assistant_message": msg,
        "chips": chips,
        "slots_filled": slots_filled,
        "handoff": journey.handoff,
        "handoff_reason": journey.handoff_reason,
        "llm_used": bool(text)
    }
