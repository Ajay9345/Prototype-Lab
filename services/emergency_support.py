import math
from typing import Dict, List, Optional

EMERGENCY_CONTACTS = {
    "ambulance": "108", "police": "100", "fire": "101",
    "women_helpline": "1091", "child_helpline": "1098", "disaster_management": "108",
}

DISTRESS_KEYWORDS = [
    "help", "emergency", "heart attack", "stroke", "bleeding",
    "accident", "pain", "breathing", "unconscious", "falling",
    "bachao", "madad", "ambulance",
]

HOSPITALS = [
    {"name": "AIIMS Delhi",               "address": "Ansari Nagar, New Delhi 110029",             "phone": "011-26588500", "type": "Government", "emergency": True, "lat": 28.5672, "lon": 77.2100},
    {"name": "Apollo Hospital Delhi",     "address": "Sarita Vihar, Delhi 110076",                 "phone": "011-26825858", "type": "Private",    "emergency": True, "lat": 28.5355, "lon": 77.2860},
    {"name": "Fortis Hospital Bangalore", "address": "154/9, Bannerghatta Road, Bangalore 560076", "phone": "080-66214444", "type": "Private",    "emergency": True, "lat": 12.9010, "lon": 77.5990},
    {"name": "Manipal Hospital Bangalore","address": "98, HAL Airport Road, Bangalore 560017",    "phone": "080-25023344", "type": "Private",    "emergency": True, "lat": 12.9576, "lon": 77.6450},
    {"name": "Lilavati Hospital Mumbai",  "address": "A-791, Bandra Reclamation, Mumbai 400050",  "phone": "022-26567891", "type": "Private",    "emergency": True, "lat": 19.0535, "lon": 72.8286},
    {"name": "KEM Hospital Mumbai",       "address": "Acharya Donde Marg, Parel, Mumbai 400012",  "phone": "022-24107000", "type": "Government", "emergency": True, "lat": 19.0030, "lon": 72.8420},
    {"name": "CMC Vellore",               "address": "Ida Scudder Road, Vellore 632004",           "phone": "0416-2281000", "type": "Private",    "emergency": True, "lat": 12.9252, "lon": 79.1333},
    {"name": "PGIMER Chandigarh",         "address": "Sector 12, Chandigarh 160012",               "phone": "0172-2747585", "type": "Government", "emergency": True, "lat": 30.7646, "lon": 76.7689},
    {"name": "SGPGI Lucknow",             "address": "Rae Bareli Road, Lucknow 226014",            "phone": "0522-2668700", "type": "Government", "emergency": True, "lat": 26.8291, "lon": 80.9905},
    {"name": "NIMHANS Bangalore",         "address": "Hosur Road, Bangalore 560029",               "phone": "080-26995000", "type": "Government", "emergency": True, "lat": 12.9431, "lon": 77.5967},
]

PHARMACIES = [
    {"name": "Apollo Pharmacy",               "address": "Connaught Place, New Delhi 110001",         "phone": "011-23345678", "open_24_7": True, "lat": 28.6304, "lon": 77.2177},
    {"name": "Guardian Pharmacy",             "address": "Sector 18, Noida 201301",                   "phone": "0120-4321098", "open_24_7": True, "lat": 28.5700, "lon": 77.3200},
    {"name": "MedPlus 24Hr",                  "address": "Lajpat Nagar, New Delhi 110024",            "phone": "011-29834567", "open_24_7": True, "lat": 28.5677, "lon": 77.2433},
    {"name": "Wellness Forever",              "address": "Dwarka Sector 10, New Delhi 110075",        "phone": "011-28041234", "open_24_7": True, "lat": 28.5921, "lon": 77.0460},
    {"name": "Jan Aushadhi Kendra",           "address": "Rohini Sector 3, New Delhi 110085",         "phone": "011-27051234", "open_24_7": True, "lat": 28.7041, "lon": 77.1025},
    {"name": "Apollo Pharmacy Gurgaon",       "address": "DLF Phase 1, Gurgaon 122002",               "phone": "0124-4321234", "open_24_7": True, "lat": 28.4595, "lon": 77.0266},
    {"name": "Fortis Pharmacy",               "address": "Vasant Kunj, New Delhi 110070",             "phone": "011-42776222", "open_24_7": True, "lat": 28.5244, "lon": 77.1580},
    {"name": "Wellness Forever Bandra",       "address": "Linking Road, Bandra West, Mumbai 400050",  "phone": "022-26401234", "open_24_7": True, "lat": 19.0600, "lon": 72.8330},
    {"name": "Noble Plus Juhu",               "address": "Juhu Tara Road, Mumbai 400049",             "phone": "022-26105678", "open_24_7": True, "lat": 19.1000, "lon": 72.8250},
    {"name": "Apollo Pharmacy Andheri",       "address": "Andheri West, Mumbai 400058",               "phone": "022-26731234", "open_24_7": True, "lat": 19.1197, "lon": 72.8464},
    {"name": "MedPlus Dadar",                 "address": "Dadar West, Mumbai 400028",                 "phone": "022-24321234", "open_24_7": True, "lat": 19.0178, "lon": 72.8478},
    {"name": "Sahakari Bhandar Pharmacy",     "address": "Prabhadevi, Mumbai 400025",                 "phone": "022-24361234", "open_24_7": True, "lat": 19.0072, "lon": 72.8258},
    {"name": "Lifeline Pharmacy",             "address": "Borivali West, Mumbai 400092",              "phone": "022-28911234", "open_24_7": True, "lat": 19.2307, "lon": 72.8567},
    {"name": "MedPlus Indiranagar",           "address": "Indiranagar, Bangalore 560038",             "phone": "080-25256789", "open_24_7": True, "lat": 12.9716, "lon": 77.6412},
    {"name": "PharmEasy Koramangala",         "address": "Koramangala, Bangalore 560034",             "phone": "080-45678901", "open_24_7": True, "lat": 12.9350, "lon": 77.6200},
    {"name": "Apollo Pharmacy Jayanagar",     "address": "Jayanagar 4th Block, Bangalore 560041",    "phone": "080-26561234", "open_24_7": True, "lat": 12.9250, "lon": 77.5938},
    {"name": "Wellness Forever HSR",          "address": "HSR Layout, Bangalore 560102",              "phone": "080-41231234", "open_24_7": True, "lat": 12.9116, "lon": 77.6389},
    {"name": "Netmeds Store Whitefield",      "address": "Whitefield, Bangalore 560066",              "phone": "080-28451234", "open_24_7": True, "lat": 12.9698, "lon": 77.7500},
    {"name": "MedPlus Malleshwaram",          "address": "Malleshwaram, Bangalore 560003",            "phone": "080-23561234", "open_24_7": True, "lat": 13.0035, "lon": 77.5710},
    {"name": "Netmeds T Nagar",               "address": "T Nagar, Chennai 600017",                   "phone": "044-24345678", "open_24_7": True, "lat": 13.0400, "lon": 80.2300},
    {"name": "Apollo Pharmacy Anna Nagar",    "address": "Anna Nagar, Chennai 600040",                "phone": "044-26211234", "open_24_7": True, "lat": 13.0850, "lon": 80.2101},
    {"name": "MedPlus Adyar",                 "address": "Adyar, Chennai 600020",                     "phone": "044-24411234", "open_24_7": True, "lat": 13.0012, "lon": 80.2565},
    {"name": "Wellness Pharmacy Velachery",   "address": "Velachery, Chennai 600042",                 "phone": "044-22431234", "open_24_7": True, "lat": 12.9815, "lon": 80.2180},
    {"name": "Apollo Pharmacy Banjara Hills", "address": "Banjara Hills, Hyderabad 500034",           "phone": "040-23541234", "open_24_7": True, "lat": 17.4156, "lon": 78.4347},
    {"name": "MedPlus Ameerpet",              "address": "Ameerpet, Hyderabad 500016",                "phone": "040-23741234", "open_24_7": True, "lat": 17.4374, "lon": 78.4487},
    {"name": "Wellness Pharmacy Gachibowli",  "address": "Gachibowli, Hyderabad 500032",              "phone": "040-23001234", "open_24_7": True, "lat": 17.4401, "lon": 78.3489},
    {"name": "Hetero Pharmacy Secunderabad",  "address": "Secunderabad, Hyderabad 500003",            "phone": "040-27891234", "open_24_7": True, "lat": 17.4399, "lon": 78.4983},
    {"name": "Frank Ross Pharmacy",           "address": "Park Street, Kolkata 700016",               "phone": "033-22291234", "open_24_7": True, "lat": 22.5550, "lon": 88.3500},
    {"name": "Apollo Pharmacy Salt Lake",     "address": "Salt Lake Sector V, Kolkata 700091",        "phone": "033-23571234", "open_24_7": True, "lat": 22.5800, "lon": 88.4300},
    {"name": "MedPlus Behala",                "address": "Behala, Kolkata 700060",                    "phone": "033-24011234", "open_24_7": True, "lat": 22.4900, "lon": 88.3100},
    {"name": "Apollo Pharmacy Kothrud",       "address": "Kothrud, Pune 411038",                      "phone": "020-25381234", "open_24_7": True, "lat": 18.5074, "lon": 73.8077},
    {"name": "MedPlus Viman Nagar",           "address": "Viman Nagar, Pune 411014",                  "phone": "020-26631234", "open_24_7": True, "lat": 18.5679, "lon": 73.9143},
    {"name": "Wellness Pharmacy Hinjewadi",   "address": "Hinjewadi, Pune 411057",                    "phone": "020-22931234", "open_24_7": True, "lat": 18.5912, "lon": 73.7389},
    {"name": "Apollo Pharmacy CG Road",       "address": "CG Road, Ahmedabad 380006",                 "phone": "079-26401234", "open_24_7": True, "lat": 23.0300, "lon": 72.5600},
    {"name": "MedPlus Satellite",             "address": "Satellite, Ahmedabad 380015",               "phone": "079-26761234", "open_24_7": True, "lat": 23.0200, "lon": 72.5100},
    {"name": "Apollo Pharmacy Malviya Nagar", "address": "Malviya Nagar, Jaipur 302017",              "phone": "0141-2721234", "open_24_7": True, "lat": 26.8500, "lon": 75.8100},
    {"name": "MedPlus Vaishali Nagar",        "address": "Vaishali Nagar, Jaipur 302021",             "phone": "0141-2351234", "open_24_7": True, "lat": 26.9100, "lon": 75.7400},
    {"name": "Apollo Pharmacy Hazratganj",    "address": "Hazratganj, Lucknow 226001",                "phone": "0522-2231234", "open_24_7": True, "lat": 26.8467, "lon": 80.9462},
    {"name": "MedPlus Gomti Nagar",           "address": "Gomti Nagar, Lucknow 226010",               "phone": "0522-2761234", "open_24_7": True, "lat": 26.8600, "lon": 81.0000},
    {"name": "Apollo Pharmacy Sector 17",     "address": "Sector 17, Chandigarh 160017",              "phone": "0172-2701234", "open_24_7": True, "lat": 30.7400, "lon": 76.7800},
    {"name": "MedPlus Sector 22",             "address": "Sector 22, Chandigarh 160022",              "phone": "0172-2741234", "open_24_7": True, "lat": 30.7300, "lon": 76.7900},
    {"name": "Apollo Pharmacy MG Road",       "address": "MG Road, Kochi 682016",                     "phone": "0484-2381234", "open_24_7": True, "lat": 9.9312,  "lon": 76.2673},
    {"name": "MedPlus Edapally",              "address": "Edapally, Kochi 682024",                    "phone": "0484-2551234", "open_24_7": True, "lat": 10.0200, "lon": 76.3100},
    {"name": "Apollo Pharmacy Vijay Nagar",   "address": "Vijay Nagar, Indore 452010",                "phone": "0731-2571234", "open_24_7": True, "lat": 22.7500, "lon": 75.8900},
    {"name": "MedPlus MP Nagar",              "address": "MP Nagar, Bhopal 462011",                   "phone": "0755-2551234", "open_24_7": True, "lat": 23.2300, "lon": 77.4300},
    {"name": "Apollo Pharmacy Dharampeth",    "address": "Dharampeth, Nagpur 440010",                 "phone": "0712-2551234", "open_24_7": True, "lat": 21.1400, "lon": 79.0700},
    {"name": "MedPlus Adajan",                "address": "Adajan, Surat 395009",                      "phone": "0261-2771234", "open_24_7": True, "lat": 21.2100, "lon": 72.8000},
    {"name": "Apollo Pharmacy RS Puram",      "address": "RS Puram, Coimbatore 641002",               "phone": "0422-2431234", "open_24_7": True, "lat": 11.0050, "lon": 76.9600},
    {"name": "MedPlus Dwaraka Nagar",         "address": "Dwaraka Nagar, Visakhapatnam 530016",       "phone": "0891-2751234", "open_24_7": True, "lat": 17.7200, "lon": 83.3100},
]

EMERGENCY_TYPE_INSTRUCTIONS = {
    "heart|chest": [
        "Have the person sit down and rest.",
        "Loosen tight clothing.",
        "If prescribed, help them take nitroglycerin.",
        "Be prepared to perform CPR if needed.",
    ],
    "breath": [
        "Help the person sit upright.",
        "Loosen tight clothing around neck and chest.",
        "Open windows for fresh air.",
        "If they have an inhaler, help them use it.",
    ],
    "bleed": [
        "Apply direct pressure to the wound.",
        "Elevate the injured area if possible.",
        "Do not remove embedded objects.",
        "Keep the person warm and calm.",
    ],
    "burn": [
        "Cool the burn with running water for 10–20 minutes.",
        "Remove jewellery and tight clothing near the burn.",
        "Do not apply ice, butter, or ointments.",
        "Cover with a clean, dry cloth.",
    ],
}

EARTH_RADIUS_KM = 6371.0
MAX_DISTANCE_KM = 200.0


class EmergencySupport:
    def detect_distress_keywords(self, text: str) -> bool:
        return any(kw in text.lower() for kw in DISTRESS_KEYWORDS)

    def get_emergency_contacts(self) -> dict:
        return EMERGENCY_CONTACTS

    def get_emergency_guidance(self, emergency_type: Optional[str] = None) -> dict:
        guidance = {
            "primary_number": "108",
            "primary_action": "Call 108 (Emergency Ambulance Service) immediately.",
            "general_instructions": [
                "Stay calm and assess the situation.",
                "Call emergency services (108) if needed.",
                "Do not move the person unless there is immediate danger.",
                "Provide clear location information to emergency services.",
                "Stay with the person until help arrives.",
            ],
            "contacts": EMERGENCY_CONTACTS,
        }
        if emergency_type:
            etype = emergency_type.lower()
            for pattern, instructions in EMERGENCY_TYPE_INSTRUCTIONS.items():
                if any(kw in etype for kw in pattern.split("|")):
                    guidance["specific_instructions"] = instructions
                    break
        return guidance

    def find_nearby_hospitals(self, lat: float, lon: float, max_results: int = 5) -> list:
        return self._find_nearby(HOSPITALS, lat, lon, max_results)

    def find_nearby_pharmacies(self, lat: float, lon: float, max_results: int = 5) -> list:
        return self._find_nearby([p for p in PHARMACIES if p.get("open_24_7")], lat, lon, max_results)

    def _find_nearby(self, locations: list, lat: float, lon: float, max_results: int) -> list:
        scored = sorted(
            [{**loc, "distance_km": round(self._haversine(lat, lon, loc["lat"], loc["lon"]), 2)} for loc in locations],
            key=lambda x: x["distance_km"],
        )
        within = [e for e in scored if e["distance_km"] <= MAX_DISTANCE_KM]
        return (within or scored)[:max_results]

    @staticmethod
    def _haversine(lat1, lon1, lat2, lon2) -> float:
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        a = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
        return EARTH_RADIUS_KM * 2 * math.asin(math.sqrt(a))


_instance: Optional[EmergencySupport] = None


def get_emergency_support() -> EmergencySupport:
    global _instance
    if _instance is None:
        _instance = EmergencySupport()
    return _instance
