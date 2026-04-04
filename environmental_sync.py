"""
Environmental Synchronizer Module
Fetches real-time environmental data (AQI, Pollen, Weather) and generates
proactive health alerts based on user-specific conditions.
"""

import os
import requests
from typing import Dict, Optional, List
from datetime import datetime

class EnvironmentalSync:
    def __init__(self):
        # API Keys (to be provided by user or set in .env)
        self.aqi_api_token = os.getenv('AQI_API_TOKEN') # e.g., WAQI
        self.weather_api_key = os.getenv('OPENWEATHER_API_KEY')

    def get_environmental_data(self, lat: float, lon: float) -> Dict:
        """
        Fetch real-time AQI and weather data for a location.
        Defaults to mock data if API keys are missing.
        """
        data = {
            "aqi": 0,
            "status": "Unknown",
            "temperature": 25,
            "humidity": 50,
            "pollutants": {},
            "timestamp": datetime.now().isoformat()
        }

        # Try WAQI (World Air Quality Index)
        if self.aqi_api_token:
            try:
                url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={self.aqi_api_token}"
                response = requests.get(url, timeout=5)
                res_data = response.json()
                if res_data.get('status') == 'ok':
                    aqi_val = res_data['data']['aqi']
                    data["aqi"] = aqi_val
                    data["status"] = self._get_aqi_status(aqi_val)
                    data["pollutants"] = res_data['data'].get('iaqi', {})
            except Exception as e:
                print(f"AQI Fetch Error: {e}")

        # If data is still default (mock), let's provide a simulation
        if data["aqi"] == 0:
            data["aqi"] = 145 # Moderate/Unhealthy for sensitive groups
            data["status"] = "Unhealthy for Sensitive Groups"
            data["is_mock"] = True

        return data

    def _get_aqi_status(self, aqi: int) -> str:
        if aqi <= 50: return "Good"
        if aqi <= 100: return "Moderate"
        if aqi <= 150: return "Unhealthy for Sensitive Groups"
        if aqi <= 200: return "Unhealthy"
        if aqi <= 300: return "Very Unhealthy"
        return "Hazardous"

    def generate_alerts(self, env_data: Dict, user_profile: Dict) -> List[Dict]:
        """
        Correlate environmental data with user profile to generate specific alerts.
        """
        alerts = []
        aqi = env_data.get('aqi', 0)
        conditions = [c.lower() for c in user_profile.get('conditions', [])]
        
        # Respiratory Alerts
        if aqi > 100:
            if any(c in conditions for c in ['asthma', 'copd', 'bronchitis', 'respiratory']):
                alerts.append({
                    "type": "high",
                    "title": "Air Quality Alert (Respiratory Risk)",
                    "message": f"AQI is {aqi} ({env_data['status']}). Given your history of respiratory issues, please limit outdoor exposure today and keep your inhaler handy.",
                    "icon": "🌬️"
                })
            elif aqi > 150:
                 alerts.append({
                    "type": "medium",
                    "title": "Poor Air Quality",
                    "message": f"AQI is reached {aqi}. It is recommended to use a mask outdoors today.",
                    "icon": "😷"
                })

        # Weather/Humidity Alerts (e.g., for Joints/Arthritis)
        humidity = env_data.get('humidity', 50)
        temp = env_data.get('temperature', 25)
        
        if humidity > 80 and any(c in conditions for c in ['arthritis', 'joint pain', 'inflammation']):
            alerts.append({
                "type": "low",
                "title": "Joint Pain Precaution",
                "message": "High humidity detected. This may trigger joint stiffness. Consider light stretching and staying warm.",
                "icon": "🦴"
            })
            
        return alerts

_env_sync_instance = None

def get_environmental_sync() -> EnvironmentalSync:
    global _env_sync_instance
    if _env_sync_instance is None:
        _env_sync_instance = EnvironmentalSync()
    return _env_sync_instance
