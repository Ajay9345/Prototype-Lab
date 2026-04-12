import os
import requests
from datetime import datetime
from typing import Dict, List, Optional

AQI_LEVELS = [(50, "Good"), (100, "Moderate"), (150, "Unhealthy for Sensitive Groups"), (200, "Unhealthy"), (300, "Very Unhealthy")]
MOCK_AQI = 145


class EnvironmentalSync:
    def __init__(self):
        self.aqi_api_token = os.getenv("AQI_API_TOKEN")

    def get_environmental_data(self, lat: float, lon: float) -> Dict:
        data = {"aqi": 0, "status": "Unknown", "temperature": 25, "humidity": 50, "pollutants": {}, "timestamp": datetime.now().isoformat()}

        if self.aqi_api_token:
            try:
                resp = requests.get(f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={self.aqi_api_token}", timeout=5).json()
                if resp.get("status") == "ok":
                    data["aqi"]       = resp["data"]["aqi"]
                    data["status"]    = self._aqi_label(data["aqi"])
                    data["pollutants"]= resp["data"].get("iaqi", {})
            except Exception as e:
                print(f"AQI fetch error: {e}")

        if data["aqi"] == 0:
            data.update({"aqi": MOCK_AQI, "status": self._aqi_label(MOCK_AQI), "is_mock": True})

        return data

    def generate_alerts(self, env_data: Dict, user_profile: Dict) -> List[Dict]:
        alerts = []
        aqi        = env_data.get("aqi", 0)
        conditions = [c.lower() for c in user_profile.get("conditions", [])]
        humidity   = env_data.get("humidity", 50)

        if aqi > 100:
            if any(c in conditions for c in {"asthma", "copd", "bronchitis", "respiratory"}):
                alerts.append({"type": "high", "title": "Air Quality Alert (Respiratory Risk)", "message": f"AQI is {aqi} ({env_data['status']}). Given your respiratory history, please limit outdoor exposure today and keep your inhaler handy.", "icon": "🌬️"})
            elif aqi > 150:
                alerts.append({"type": "medium", "title": "Poor Air Quality", "message": f"AQI has reached {aqi}. It is recommended to wear a mask outdoors today.", "icon": "😷"})

        if humidity > 80 and any(c in conditions for c in {"arthritis", "joint pain", "inflammation"}):
            alerts.append({"type": "low", "title": "Joint Pain Precaution", "message": "High humidity detected. This may trigger joint stiffness. Consider light stretching and staying warm.", "icon": "🦴"})

        return alerts

    @staticmethod
    def _aqi_label(aqi: int) -> str:
        for threshold, label in AQI_LEVELS:
            if aqi <= threshold:
                return label
        return "Hazardous"


_instance: Optional[EnvironmentalSync] = None


def get_environmental_sync() -> EnvironmentalSync:
    global _instance
    if _instance is None:
        _instance = EnvironmentalSync()
    return _instance
