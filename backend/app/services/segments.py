from typing import Dict, Any, Optional
from rapidfuzz import fuzz

SEGMENTS = [
    "Micro retail & services",
    "Professional offices",
    "Small multi-site businesses",
    "Small manufacturers",
]

# Business type to majority segment
BUSINESS_TYPE_TO_SEGMENT = {
    # Micro retail & services
    "Bakery": "Micro retail & services",
    "Boutique": "Micro retail & services",
    "Hardware store": "Micro retail & services",
    "Kirana store": "Micro retail & services",
    "Mobile repair shop": "Micro retail & services",
    "Optician": "Micro retail & services",
    "Pharmacy": "Micro retail & services",
    "Salon": "Micro retail & services",
    "Stationery shop": "Micro retail & services",
    "Sweet shop": "Micro retail & services",
    # Professional offices
    "Architecture studio": "Professional offices",
    "CA firm": "Professional offices",
    "Coaching centre": "Professional offices",
    "Dental clinic": "Professional offices",
    "Diagnostic lab": "Professional offices",
    "Insurance agency": "Professional offices",
    "Law office": "Professional offices",
    "Physiotherapy clinic": "Professional offices",
    "Real estate agency": "Professional offices",
    "Travel agency": "Professional offices",
    # Small multi-site businesses
    "Apparel retail chain": "Small multi-site businesses",
    "Bakery chain": "Small multi-site businesses",
    "Budget hotel group": "Small multi-site businesses",
    "Electronics retail chain": "Small multi-site businesses",
    "Gym chain": "Small multi-site businesses",
    "Pharmacy chain": "Small multi-site businesses",
    "Pre-school chain": "Small multi-site businesses",
    "Restaurant chain": "Small multi-site businesses",
    # Small manufacturers
    "Auto-parts unit": "Small manufacturers",
    "Food processing unit": "Small manufacturers",
    "Furniture workshop": "Small manufacturers",
    "Packaging unit": "Small manufacturers",
    "Plastic moulding unit": "Small manufacturers",
    "Printing press": "Small manufacturers",
    "Textile unit": "Small manufacturers",
}

KEYWORD_MAPPINGS = [
    # Professional
    (["dental", "dentist", "tooth"], "Dental clinic", "Professional offices", "We found you as a dental clinic"),
    (["physio", "rehab", "therapy"], "Physiotherapy clinic", "Professional offices", "We identified your business as a physiotherapy clinic"),
    (["advocate", "law", "legal", "solicitor", "attorney"], "Law office", "Professional offices", "We found you as a legal/law practice"),
    (["ca ", "chartered", "accountant", "audit", "taxation", "accounting"], "CA firm", "Professional offices", "We identified you as an accounting/CA firm"),
    (["architect", "interior design", "architecture"], "Architecture studio", "Professional offices", "We found you as an architecture/design studio"),
    (["lab", "pathology", "diagnostic", "imaging", "scan"], "Diagnostic lab", "Professional offices", "We identified you as a diagnostic lab"),
    (["travel", "tours", "tourism", "holidays"], "Travel agency", "Professional offices", "We found you as a travel agency"),
    (["insurance", "brokerage", "underwriter"], "Insurance agency", "Professional offices", "We identified you as an insurance agency"),
    (["coaching", "academy", "classes", "tuition", "institute"], "Coaching centre", "Professional offices", "We identified you as an educational/coaching centre"),
    (["real estate", "realty", "properties", "property"], "Real estate agency", "Professional offices", "We found you as a real estate agency"),
    # Multi-site keywords
    (["chain", "branches", "outlets", "group of hotels", "hotel group"], "Budget hotel group", "Small multi-site businesses", "Identified as a multi-location enterprise"),
    (["hotel", "residency", "inn", "suites", "lodge"], "Budget hotel group", "Small multi-site businesses", "Identified as a hospitality business"),
    (["gym", "fitness", "crossfit", "workout"], "Gym chain", "Small multi-site businesses", "Identified as a fitness facility"),
    (["pre-school", "kindergarten", "play school", "nursery"], "Pre-school chain", "Small multi-site businesses", "Identified as an education centre"),
    # Manufacturing
    (["textile", "fabrics", "weaving", "spinning", "garment manufacturing"], "Textile unit", "Small manufacturers", "Identified as a textile manufacturer"),
    (["plastic", "moulding", "polymers", "extrusion"], "Plastic moulding unit", "Small manufacturers", "Identified as a plastic moulding unit"),
    (["printing", "press", "printers", "publishing"], "Printing press", "Small manufacturers", "Identified as a printing press"),
    (["packaging", "boxes", "corrugated", "cartons"], "Packaging unit", "Small manufacturers", "Identified as a packaging unit"),
    (["auto parts", "automotive", "ancillary", "gears", "precision"], "Auto-parts unit", "Small manufacturers", "Identified as an auto-parts manufacturing unit"),
    (["food processing", "agro processing", "grain mill", "flour mill", "oil mill"], "Food processing unit", "Small manufacturers", "Identified as a food processing unit"),
    (["furniture", "woodwork", "woodcraft", "wood", "craft", "carpentry", "timber"], "Furniture workshop", "Small manufacturers", "Identified as a furniture workshop"),
    (["manufacturing", "industries", "works", "factory", "engineering"], "Manufacturing unit", "Small manufacturers", "Identified as a manufacturing enterprise"),
    # Micro Retail
    (["kirana", "provision", "general store", "grocery"], "Kirana store", "Micro retail & services", "We found you as a grocery / kirana store"),
    (["bakery", "bake", "confectionery", "cakes"], "Bakery", "Micro retail & services", "We found you as a bakery"),
    (["sweet", "mithai", "halwai"], "Sweet shop", "Micro retail & services", "We found you as a sweet / confectionery shop"),
    (["pharmacy", "medical store", "druggist", "chemist"], "Pharmacy", "Micro retail & services", "We found you as a pharmacy / chemist"),
    (["optician", "eyewear", "optical", "opticals"], "Optician", "Micro retail & services", "We found you as an eyewear / optician store"),
    (["salon", "beauty parlour", "barber", "spa", "hair"], "Salon", "Micro retail & services", "We found you as a salon / personal care business"),
    (["hardware", "sanitary", "paints", "electricals", "tools"], "Hardware store", "Micro retail & services", "We found you as a hardware & building materials store"),
    (["stationery", "book depot", "xerox", "photocopy"], "Stationery shop", "Micro retail & services", "We found you as a stationery & print store"),
    (["boutique", "fashion", "tailor", "garments", "cloth"], "Boutique", "Micro retail & services", "We found you as an apparel / boutique store"),
    (["mobile repair", "telecom store", "mobile accessories"], "Mobile repair shop", "Micro retail & services", "We found you as a mobile repair & electronics store"),
]

def infer_segment(
    trade_name: Optional[str] = None,
    legal_name: Optional[str] = None,
    nic_description: Optional[str] = None,
    enterprise_type: Optional[str] = None,
    major_activity: Optional[str] = None,
    sites: int = 1,
    employees: int = 1
) -> Dict[str, Any]:
    text_corpus = " ".join([
        (trade_name or ""),
        (legal_name or ""),
        (nic_description or ""),
        (major_activity or "")
    ]).lower()

    # Rule 2: Override by size answers
    if sites >= 2:
        return {
            "segment": "Small multi-site businesses",
            "confidence": 0.95,
            "reason_key": "sites_ge_2",
            "reason_display": f"Multiple operational locations ({sites} sites)"
        }
    
    if employees >= 10 and (
        "manufactur" in text_corpus or 
        "product" in text_corpus or 
        (major_activity and "manufactur" in major_activity.lower())
    ):
        return {
            "segment": "Small manufacturers",
            "confidence": 0.95,
            "reason_key": "mfg_employees_ge_10",
            "reason_display": f"Manufacturing operation with {employees} employees"
        }

    # Rule 1: Match keywords
    best_match = None
    for keywords, b_type, segment, display in KEYWORD_MAPPINGS:
        for kw in keywords:
            if kw in text_corpus:
                return {
                    "segment": segment,
                    "confidence": 0.90,
                    "reason_key": f"kw_{kw.replace(' ', '_')}",
                    "reason_display": display
                }

    # Udyam activity / enterprise_type hints
    if major_activity and "manufactur" in major_activity.lower():
        return {
            "segment": "Small manufacturers",
            "confidence": 0.85,
            "reason_key": "udyam_manufacturing",
            "reason_display": "Udyam registration records manufacturing activity"
        }
    if major_activity and "service" in major_activity.lower():
        if enterprise_type in ["Small", "Medium"] or employees >= 5:
            return {
                "segment": "Professional offices",
                "confidence": 0.80,
                "reason_key": "udyam_services_office",
                "reason_display": "Udyam registration records professional services"
            }
        return {
            "segment": "Micro retail & services",
            "confidence": 0.80,
            "reason_key": "udyam_micro_service",
            "reason_display": "Udyam registration records micro-retail / services"
        }

    # Fallback default
    return {
        "segment": "Micro retail & services",
        "confidence": 0.60,
        "reason_key": "default_starter",
        "reason_display": "Standard business profile"
    }
