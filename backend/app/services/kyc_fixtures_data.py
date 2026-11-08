from typing import Dict, Any

FIXTURES_DATA: Dict[str, Dict[str, Any]] = {
    "K01": {
        "applicant_name": "Vindhya Tours & Travels",
        "gst_cert": {
            "gstin": "37IHKXV5167L1ZS",
            "legal_name": "Neha Kaur (Prop. Vindhya Tours & Travels)",
            "trade_name": "Vindhya Tours & Travels",
            "constitution": "Proprietorship",
            "address": "Shop/Unit 1, Tech Park Road, Visakhapatnam, Andhra Pradesh - 118383",
            "state": "Andhra Pradesh",
            "confidence": 0.95
        },
        "udyam_cert": {
            "udyam_number": "",  # Missing on specimen
            "enterprise_name": "Vindhya Tours & Travels",
            "major_activity": "Services",
            "city": "Visakhapatnam",
            "state": "Andhra Pradesh",
            "confidence": 0.85
        },
        "signatory_id": {
            "name": "Neha Kaur",
            "designation": "Office admin",  # Soft flag
            "for_business": "Vindhya Tours & Travels",
            "id_no": "SYN-ID-346190",
            "valid_till": "2028-03-26",
            "confidence": 0.95
        },
        "address_proof": {
            "consumer_no": "9485717625",
            "billed_to": "Vindhya Tours & Travels",
            "supply_address": "Shop/Unit 1, Tech Park Road, Visakhapatnam, Andhra Pradesh - 118383",
            "state": "Andhra Pradesh",
            "bill_date": "2026-06-26",
            "confidence": 0.95
        }
    },
    "K02": {
        "applicant_name": "Harmony Dental Care",
        "gst_cert": {
            "gstin": "19E0GXH4115Y1ZL",  # Monospace confusion 0 vs O
            "legal_name": "Joseph Shah (Prop. Harmony Dental Care)",
            "trade_name": "Harmony Dental Care",
            "constitution": "Proprietorship",
            "address": "Shop/Unit 199, Station Road, Kolkata, West Bengal - 347550",
            "state": "West Bengal",
            "confidence": 0.90
        },
        "udyam_cert": {
            "udyam_number": "UDYAM-WB-00-5053330",
            "enterprise_name": "Harmony Dental Care",
            "major_activity": "Services",
            "city": "Kolkata",
            "state": "West Bengal",
            "confidence": 0.95
        },
        "signatory_id": {
            "name": "Joseph Shah",
            "designation": "Manager",  # Soft flag
            "for_business": "Harmony Dental Care",
            "id_no": "SYN-ID-816907",
            "valid_till": "2028-09-10",
            "confidence": 0.95
        },
        "address_proof": {
            "consumer_no": "9790713533",
            "billed_to": "Harmony Dental Care",
            "supply_address": "Shop/Unit 199, Station Road, Kolkata, West Bengal - 347550",
            "state": "West Bengal",
            "bill_date": "2026-05-22",
            "confidence": 0.95
        }
    },
    "K03": {
        "applicant_name": "Ganesh Woodcraft",
        "gst_cert": {
            "gstin": "27XUIXG0767D1ZP",
            "legal_name": "Joseph Singh (Prop. Ganesh Woodcraft)",
            "trade_name": "Ganesh Woodcraft",
            "constitution": "Proprietorship",
            "address": "Shop/Unit 80, Civil Lines, Nagpur, Maharashtra - 411231",
            "state": "Maharashtra",
            "confidence": 0.95
        },
        "udyam_cert": {
            "udyam_number": "UDYAM-MH-00-9516696",
            "enterprise_name": "Ganesh Woodcraft",
            "major_activity": "Manufacturing",
            "city": "Nagpur",
            "state": "Maharashtra",
            "confidence": 0.95
        },
        "signatory_id": {
            "name": "Joseph Singh",
            "designation": "Owner",
            "for_business": "Ganesh Woodcraft",
            "id_no": "SYN-ID-447889",
            "valid_till": "2028-07-04",
            "confidence": 0.95
        },
        "address_proof": {
            "consumer_no": "3438517928",
            "billed_to": "Ganesh Woodcraft",
            "supply_address": "Shop/Unit 80, Civil Lines, Nagpur, Maharashtra - 411231",
            "state": "Maharashtra",
            "bill_date": "2026-05-30",
            "confidence": 0.95
        }
    },
    "K04": {
        "applicant_name": "Saffron Dental Care LLP",
        "gst_cert": {
            "gstin": "27PZSXS1936Q1ZH",
            "legal_name": "Saffron Dental Care LLP",
            "trade_name": "Saffron Dental Care LLP",
            "constitution": "Limited Liability Partnership",
            "address": "Shop/Unit 75, Lake View Colony, Nagpur, Maharashtra - 137452",
            "state": "Maharashtra",
            "blurred": True,  # Severely blurred specimen
            "confidence": 0.45
        },
        "udyam_cert": {
            "udyam_number": "UDYAM-MH-00-4762519",
            "enterprise_name": "Saffron Dental Care LLP",
            "major_activity": "Services",
            "city": "Nagpur",
            "state": "Maharashtra",
            "confidence": 0.95
        },
        "signatory_id": {
            "name": "Saffron Dental Care Signatory",
            "designation": "Partner",
            "for_business": "Saffron Dental Care LLP",
            "id_no": "SYN-ID-918234",
            "valid_till": "2028-11-20",
            "confidence": 0.95
        },
        "address_proof": {
            "consumer_no": "7397844759",
            "billed_to": "Saffron Dental Care LLP",
            "supply_address": "Shop/Unit 75, Lake View Colony, Nagpur, Maharashtra - 137452",
            "state": "Maharashtra",
            "bill_date": "2026-05-28",
            "confidence": 0.95
        }
    },
    "K05": {
        "applicant_name": "Balaji Realty LLP",
        "gst_cert": {
            "gstin": "32TZAXB5481U1Z1",
            "legal_name": "Balaji Realty LLP",
            "trade_name": "Balaji Realty LLP",
            "constitution": "Limited Liability Partnership",
            "address": "Shop/Unit 38, Civil Lines, Kochi, Kerala - 752083",
            "state": "Kerala",
            "confidence": 0.95
        },
        "udyam_cert": {},
        "signatory_id": {
            "name": "Anita Shah",
            "designation": "Owner",
            "for_business": "Balaji Realty LLP",
            "id_no": "SYN-ID-587234",
            "valid_till": "2029-09-11",
            "confidence": 0.95
        },
        "address_proof": {
            "consumer_no": "4294969054",
            "billed_to": "Balaji Realty LLP",
            "supply_address": "Shop/Unit 38, Civil Lines, Kochi, Kerala - 752083",
            "state": "Kerala",
            "bill_date": "2026-06-11",
            "confidence": 0.95
        }
    },
    "K06": {
        "applicant_name": "Saffron Unisex Salon",
        "gst_cert": {
            "gstin": "08YKZXS8189L1Z0",  # Monospace confusion 8 vs 5 and 0 vs O
            "legal_name": "Pooja Shah (Prop. Saffron Unisex Salon)",
            "trade_name": "Saffron Unisex Salon",
            "constitution": "Proprietorship",
            "address": "Shop/Unit 71, Market Yard, Jaipur, Rajasthan - 194057",
            "state": "Rajasthan",
            "confidence": 0.95
        },
        "udyam_cert": {
            "udyam_number": "UDYAM-RJ-00-6577157",
            "enterprise_name": "Saffron Unisex Salon",
            "major_activity": "Services",
            "city": "Jaipur",
            "state": "Rajasthan",
            "confidence": 0.95
        },
        "signatory_id": {
            "name": "Pooja Shah",
            "designation": "Owner",
            "for_business": "Saffron Unisex Salon",
            "id_no": "SYN-ID-118354",
            "valid_till": "2028-09-15",
            "confidence": 0.95
        },
        "address_proof": {
            "consumer_no": "9566781101",
            "billed_to": "Saffron Unisex Salon",
            "supply_address": "Shop/Unit 71, Market Yard, Jaipur, Rajasthan - 194057",
            "state": "Rajasthan",
            "bill_date": "2026-06-11",
            "confidence": 0.95
        }
    },
    "K07": {
        "applicant_name": "Neelgiri Physio Clinic",
        "gst_cert": {
            "gstin": "07CPCXN0398P1ZT",
            "legal_name": "Neha Banerjee (Prop. Shri Physio Clinic)",  # Mismatch with trade name and registry
            "trade_name": "Neelgiri Physio Clinic",
            "constitution": "Proprietorship",
            "address": "Shop/Unit 52, Transport Nagar, Delhi, Delhi - 334596",
            "state": "Delhi",
            "confidence": 0.95
        },
        "udyam_cert": {
            "udyam_number": "UDYAM-DL-00-9565547",
            "enterprise_name": "Neelgiri Physio Clinic",
            "major_activity": "Services",
            "city": "Delhi",
            "state": "Delhi",
            "confidence": 0.95
        },
        "signatory_id": {
            "name": "Neha Banerjee",
            "designation": "Manager",  # Soft flag
            "for_business": "Neelgiri Physio Clinic",
            "id_no": "SYN-ID-178237",
            "valid_till": "2030-05-05",
            "confidence": 0.95
        },
        "address_proof": {
            "consumer_no": "7545812405",
            "billed_to": "Neelgiri Physio Clinic",
            "supply_address": "Shop/Unit 52, Transport Nagar, Delhi, Delhi - 334596",
            "state": "Delhi",
            "bill_date": "2026-07-05",
            "confidence": 0.95
        }
    },
    "K08": {
        "applicant_name": "Green Leaf Legal Associates",
        "gst_cert": {
            "gstin": "24X0RXG9365M1Z3",  # Monospace confusion 0 vs O
            "legal_name": "Joseph Rao (Prop. Green Leaf Legal Associates)",
            "trade_name": "Green Leaf Legal Associates",
            "constitution": "Proprietorship",
            "address": "Shop/Unit 238, Ring Road, Vadodara, Gujarat - 348176",
            "state": "Gujarat",
            "confidence": 0.95
        },
        "udyam_cert": {
            "udyam_number": "UDYAM-GJ-00-8477445",
            "enterprise_name": "Green Leaf Legal Associates",
            "major_activity": "Services",
            "city": "Vadodara",
            "state": "Gujarat",
            "confidence": 0.95
        },
        "signatory_id": {
            "name": "Joseph Rao",
            "designation": "Office admin",  # Soft flag
            "for_business": "Green Leaf Legal Associates",
            "id_no": "SYN-ID-393148",
            "valid_till": "2027-09-18",
            "confidence": 0.95
        },
        "address_proof": {
            "consumer_no": "2568472785",
            "billed_to": "Green Leaf Legal Associates",
            "supply_address": "Shop/Unit 238, Ring Road, Vadodara, Gujarat - 348176",
            "state": "Gujarat",
            "bill_date": "2026-05-26",
            "confidence": 0.95
        }
    },
    "K09": {
        "applicant_name": "Kaveri Insurance Advisors",
        "gst_cert": {
            "gstin": "37LDYXK0296F1ZB",
            "legal_name": "Anita Kulkarni (Prop. Kaveri Insurance Advisors)",
            "trade_name": "Kaveri Insurance Advisors",
            "constitution": "Proprietorship",
            "address": "Shop/Unit 217, Civil Lines, Visakhapatnam, Andhra Pradesh - 405337",
            "state": "Andhra Pradesh",
            "confidence": 0.95
        },
        "udyam_cert": {
            "udyam_number": "UDYAM-AP-00-9751562",
            "enterprise_name": "Kaveri Insurance Advisors",
            "major_activity": "Services",
            "city": "Visakhapatnam",
            "state": "Andhra Pradesh",
            "confidence": 0.95
        },
        "signatory_id": {
            "name": "Anita Kulkarni",
            "designation": "Office admin",  # Soft flag
            "for_business": "Kaveri Insurance Advisors",
            "id_no": "SYN-ID-126040",
            "valid_till": "2027-12-22",
            "confidence": 0.95
        },
        "address_proof": {
            "consumer_no": "9375012581",
            "billed_to": "Kaveri Insurance Advisors",
            "supply_address": "Shop/Unit 217, Civil Lines, Visakhapatnam, Andhra Pradesh - 405337",
            "state": "Andhra Pradesh",
            "bill_date": "2026-07-10",
            "confidence": 0.95
        }
    },
    "K10": {
        "applicant_name": "Kaveri Stays LLP",
        "gst_cert": {
            "gstin": "27QHJXK0658U1ZL",
            "legal_name": "Kaveri Stays LLP",
            "trade_name": "Kaveri Stays LLP",
            "constitution": "Limited Liability Partnership",
            "address": "Shop/Unit 21, Sector 14, Mumbai, Maharashtra - 570043",
            "state": "Maharashtra",
            "confidence": 0.95
        },
        "udyam_cert": {
            "udyam_number": "UDYAM-MH-00-7183141",
            "enterprise_name": "Kaveri Stays LLP",
            "major_activity": "Services",
            "city": "Mumbai",
            "state": "Maharashtra",
            "confidence": 0.95
        },
        "signatory_id": {
            "name": "Nisha Arora",
            "designation": "Owner",
            "for_business": "Kaveri Stays LLP",
            "id_no": "SYN-ID-247542",
            "valid_till": "2029-06-01",
            "confidence": 0.95
        },
        "address_proof": {
            "consumer_no": "6910330901",
            "billed_to": "Kaveri Stays LLP",
            "supply_address": "Shop/Unit 21, Sector 14, Mumbai, Maharashtra - 570043",
            "state": "Maharashtra",
            "bill_date": "2026-06-18",
            "confidence": 0.95
        }
    },
    "K11": {
        "applicant_name": "Trinity Bake House Pvt Ltd",
        "gst_cert": {
            "gstin": "03KGZXT1320R1ZZ",
            "legal_name": "Trinity Bake House Pvt Ltd",
            "trade_name": "Trinity Bake House Pvt Ltd",
            "constitution": "Private Limited Company",
            "address": "Shop/Unit 188, Industrial Area Phase 2, Ludhiana, Punjab - 541498",
            "state": "Punjab",
            "confidence": 0.95
        },
        "udyam_cert": {
            "udyam_number": "UDYAM-PB-00-8451120",
            "enterprise_name": "Trinity Bake House Pvt Ltd",
            "major_activity": "Manufacturing",
            "city": "Ludhiana",
            "state": "Punjab",
            "confidence": 0.95
        },
        "signatory_id": {
            "name": "Trinity Signatory",
            "designation": "Director",
            "for_business": "Trinity Bake House Pvt Ltd",
            "id_no": "SYN-ID-882194",
            "valid_till": "2028-08-15",
            "confidence": 0.95
        },
        "address_proof": {
            "consumer_no": "2710511786",
            "billed_to": "Trinity Bake House Pvt Ltd",
            "supply_address": "Shop/Unit 188, Industrial Area Phase 2, Ludhiana, Punjab - 541498",
            "state": "Punjab",
            "bill_date": "2025-10-31",  # 257 days old -> EXPIRED (>90 days)!
            "confidence": 0.95
        }
    },
    "K12": {
        "applicant_name": "Star Electronics",
        "gst_cert": {
            "gstin": "37NBLXS1145E1ZU",
            "legal_name": "Pooja Agarwal (Prop. Star Electronics)",
            "trade_name": "Star Electronics",
            "constitution": "Proprietorship",
            "address": "Shop/Unit 216, Nehru Nagar, Visakhapatnam, Andhra Pradesh - 762071",
            "state": "Andhra Pradesh",
            "confidence": 0.95
        },
        "udyam_cert": {
            "udyam_number": "UDYAM-AP-00-5186772",
            "enterprise_name": "Star Electronics",
            "major_activity": "Services",
            "city": "Visakhapatnam",
            "state": "Andhra Pradesh",
            "confidence": 0.95
        },
        "signatory_id": {
            "name": "Pooja Agarwal",
            "designation": "Owner",
            "for_business": "Star Electronics",
            "id_no": "SYN-ID-365512",
            "valid_till": "2029-03-03",
            "confidence": 0.95
        },
        "address_proof": {
            "consumer_no": "6982457282",
            "billed_to": "Star Electronics",
            "supply_address": "Shop/Unit 216, Nehru Nagar, Visakhapatnam, Andhra Pradesh - 762071",
            "state": "Andhra Pradesh",
            "bill_date": "2026-07-06",
            "confidence": 0.95
        }
    }
}
