import os
import requests
from datetime import datetime
from typing import Dict, List, Optional

# AQI level labels
AQI_LEVELS = [
    (50,  "Good"),
    (100, "Moderate"),
    (150, "Unhealthy for Sensitive Groups"),
    (200, "Unhealthy"),
    (300, "Very Unhealthy"),
]

# Fallback AQI used when no API key is configured
MOCK_AQI = 145


class EnvironmentalSync:
    """
    Fetches real-time Air Quality Index (AQI) data for a location
    and generates health alerts based on the user's conditions.

    Requires AQI_API_TOKEN in the environment for live data.
    Falls back to a simulated value when the key is absent.
    """

    def __init__(self):
        self.aqi_api_token = os.getenv("AQI_API_TOKEN")

    def get_environmental_data(self, lat: float, lon: float) -> Dict:
        """
        Fetch AQI data for the given coordinates.

        Returns a dict with: aqi, status, temperature, humidity,
        pollutants, timestamp, and optionally is_mock=True.
        """
        data = {
            "aqi":         0,
            "status":      "Unknown",
            "temperature": 25,
            "humidity":    50,
            "pollutants":  {},
            "timestamp":   datetime.now().isoformat(),
        }

        if self.aqi_api_token:
            try:
                url      = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={self.aqi_api_token}"
                response = requests.get(url, timeout=5).json()
                if response.get("status") == "ok":
                    aqi_val          = response["data"]["aqi"]
                    data["aqi"]      = aqi_val
                    data["status"]   = self._aqi_label(aqi_val)
                    data["pollutants"] = response["data"].get("iaqi", {})
            except Exception as e:
                print(f"AQI fetch error: {e}")

        # Use mock data if the live fetch returned nothing
        if data["aqi"] == 0:
            data["aqi"]     = MOCK_AQI
            data["status"]  = self._aqi_label(MOCK_AQI)
            data["is_mock"] = True

        return data

    def generate_alerts(self, env_data: Dict, user_profile: Dict) -> List[Dict]:
        """
        Compare environmental data against the user's conditions and
        return a list of relevant health alerts.
        """
        alerts: List[Dict] = []
        aqi        = env_data.get("aqi", 0)
        conditions = [c.lower() for c in user_profile.get("conditions", [])]
        humidity   = env_data.get("humidity", 50)

        # Respiratory alert for high AQI
        if aqi > 100:
            respiratory_conditions = {"asthma", "copd", "bronchitis", "respiratory"}
            if any(c in conditions for c in respiratory_conditions):
                alerts.append({
                    "type":    "high",
                    "title":   "Air Quality Alert (Respiratory Risk)",
                    "message": (
                        f"AQI is {aqi} ({env_data['status']}). Given your respiratory history, "
                        "please limit outdoor exposure today and keep your inhaler handy."
                    ),
                    "icon": "🌬️",
                })
            elif aqi > 150:
                alerts.append({
                    "type":    "medium",
                    "title":   "Poor Air Quality",
                    "message": f"AQI has reached {aqi}. It is recommended to wear a mask outdoors today.",
                    "icon":    "😷",
                })

        # Joint pain alert for high humidity
        joint_conditions = {"arthritis", "joint pain", "inflammation"}
        if humidity > 80 and any(c in conditions for c in joint_conditions):
            alerts.append({
                "type":    "low",
                "title":   "Joint Pain Precaution",
                "message": "High humidity detected. This may trigger joint stiffness. Consider light stretching and staying warm.",
                "icon":    "🦴",
            })

        return alerts

    # ── Private helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _aqi_label(aqi: int) -> str:
        """Map a numeric AQI value to its descriptive label."""
        for threshold, label in AQI_LEVELS:
            if aqi <= threshold:
                return label
        return "Hazardous"


# ── Singleton accessor ────────────────────────────────────────────────────────
_instance: Optional[EnvironmentalSync] = None


def get_environmental_sync() -> EnvironmentalSync:
    """Return the shared EnvironmentalSync instance."""
    global _instance
    if _instance is None:
        _instance = EnvironmentalSync()
    return _instance
