"""
Emergency Support Module
Provides emergency detection, hospital location services,
and emergency contact information.
"""

from typing import Dict, List, Optional, Tuple
import math


class EmergencySupport:
    def __init__(self):
        # India emergency numbers
        self.emergency_contacts = {
            'ambulance': '108',
            'police': '100',
            'fire': '101',
            'women_helpline': '1091',
            'child_helpline': '1098',
            'disaster_management': '108'
        }
        
        # Static database of major hospitals in India 
        
        self.hospitals_database = [
            {
                'name': 'AIIMS Delhi',
                'address': 'Ansari Nagar, New Delhi, Delhi 110029',
                'phone': '011-26588500',
                'type': 'Government',
                'emergency': True,
                'lat': 28.5672,
                'lon': 77.2100
            },
            {
                'name': 'Apollo Hospital Delhi',
                'address': 'Sarita Vihar, Delhi 110076',
                'phone': '011-26825858',
                'type': 'Private',
                'emergency': True,
                'lat': 28.5355,
                'lon': 77.2860
            },
            {
                'name': 'Fortis Hospital Bangalore',
                'address': '154/9, Bannerghatta Road, Bangalore 560076',
                'phone': '080-66214444',
                'type': 'Private',
                'emergency': True,
                'lat': 12.9010,
                'lon': 77.5990
            },
            {
                'name': 'Manipal Hospital Bangalore',
                'address': '98, HAL Airport Road, Bangalore 560017',
                'phone': '080-25023344',
                'type': 'Private',
                'emergency': True,
                'lat': 12.9576,
                'lon': 77.6450
            },
            {
                'name': 'Lilavati Hospital Mumbai',
                'address': 'A-791, Bandra Reclamation, Mumbai 400050',
                'phone': '022-26567891',
                'type': 'Private',
                'emergency': True,
                'lat': 19.0535,
                'lon': 72.8286
            },
            {
                'name': 'KEM Hospital Mumbai',
                'address': 'Acharya Donde Marg, Parel, Mumbai 400012',
                'phone': '022-24107000',
                'type': 'Government',
                'emergency': True,
                'lat': 19.0030,
                'lon': 72.8420
            },
            {
                'name': 'CMC Vellore',
                'address': 'Ida Scudder Road, Vellore, Tamil Nadu 632004',
                'phone': '0416-2281000',
                'type': 'Private',
                'emergency': True,
                'lat': 12.9252,
                'lon': 79.1333
            },
            {
                'name': 'PGIMER Chandigarh',
                'address': 'Sector 12, Chandigarh 160012',
                'phone': '0172-2747585',
                'type': 'Government',
                'emergency': True,
                'lat': 30.7646,
                'lon': 76.7689
            },
            {
                'name': 'SGPGI Lucknow',
                'address': 'Rae Bareli Road, Lucknow, Uttar Pradesh 226014',
                'phone': '0522-2668700',
                'type': 'Government',
                'emergency': True,
                'lat': 26.8291,
                'lon': 80.9905
            },
            {
                'name': 'NIMHANS Bangalore',
                'address': 'Hosur Road, Bangalore 560029',
                'phone': '080-26995000',
                'type': 'Government',
                'emergency': True,
                'lat': 12.9431,
                'lon': 77.5967
            }
        ]
        
        # Mock database of 24/7 Pharmacies
        self.pharmacies_database = [
            {
                'name': 'Apollo Pharmacy 24/7',
                'address': 'Connaught Place, New Delhi, Delhi 110001',
                'phone': '011-23345678',
                'open_24_7': True,
                'lat': 28.6304,
                'lon': 77.2177
            },
            {
                'name': 'Wellness Forever',
                'address': 'Linking Road, Bandra West, Mumbai 400050',
                'phone': '022-26401234',
                'open_24_7': True,
                'lat': 19.0600,
                'lon': 72.8330
            },
            {
                'name': 'MedPlus Pharmacy',
                'address': 'Indiranagar, Bangalore 560038',
                'phone': '080-25256789',
                'open_24_7': True,
                'lat': 12.9716,
                'lon': 77.6412
            },
            {
                'name': 'Frank Ross Pharmacy',
                'address': 'Park Street, Kolkata 700016',
                'phone': '033-22291234',
                'open_24_7': True,
                'lat': 22.5550,
                'lon': 88.3500
            },
            {
                'name': 'Noble Plus',
                'address': 'Juhu Tara Road, Mumbai 400049',
                'phone': '022-26105678',
                'open_24_7': True,
                'lat': 19.1000,
                'lon': 72.8250
            },
            {
                'name': 'Guardian Pharmacy',
                'address': 'Sector 18, Noida 201301',
                'phone': '0120-4321098',
                'open_24_7': True,
                'lat': 28.5700,
                'lon': 77.3200
            },
            {
                'name': 'Netmeds Pharmacy',
                'address': 'T Nagar, Chennai 600017',
                'phone': '044-24345678',
                'open_24_7': True,
                'lat': 13.0400,
                'lon': 80.2300
            },
            {
                'name': 'PharmEasy Store',
                'address': 'Koramangala, Bangalore 560034',
                'phone': '080-45678901',
                'open_24_7': True,
                'lat': 12.9350,
                'lon': 77.6200
            }
        ]
    
    def get_emergency_contacts(self) -> Dict[str, str]:
        """Get all emergency contact numbers."""
        return self.emergency_contacts
    
    def get_emergency_guidance(self, emergency_type: Optional[str] = None) -> Dict:
        """
        Get emergency guidance and instructions.
        
        Args:
            emergency_type: Type of emergency (optional)
            
        Returns:
            Dictionary with emergency guidance
        """
        guidance = {
            'primary_number': '108',
            'primary_action': 'Call 108 (Emergency Ambulance Service) immediately',
            'general_instructions': [
                'Stay calm and assess the situation',
                'Call emergency services (108) if needed',
                'Do not move the person unless there is immediate danger',
                'Provide clear location information to emergency services',
                'Stay with the person until help arrives'
            ],
            'contacts': self.emergency_contacts
        }
        
        # Add specific guidance based on emergency type
        if emergency_type:
            emergency_type_lower = emergency_type.lower()
            
            if 'heart' in emergency_type_lower or 'chest' in emergency_type_lower:
                guidance['specific_instructions'] = [
                    'Have the person sit down and rest',
                    'Loosen tight clothing',
                    'If prescribed, help them take nitroglycerin',
                    'Be prepared to perform CPR if needed'
                ]
            elif 'breath' in emergency_type_lower:
                guidance['specific_instructions'] = [
                    'Help the person sit upright',
                    'Loosen tight clothing around neck and chest',
                    'Open windows for fresh air',
                    'If they have an inhaler, help them use it'
                ]
            elif 'bleed' in emergency_type_lower:
                guidance['specific_instructions'] = [
                    'Apply direct pressure to the wound',
                    'Elevate the injured area if possible',
                    'Do not remove embedded objects',
                    'Keep the person warm and calm'
                ]
            elif 'burn' in emergency_type_lower:
                guidance['specific_instructions'] = [
                    'Cool the burn with running water for 10-20 minutes',
                    'Remove jewelry and tight clothing near the burn',
                    'Do not apply ice, butter, or ointments',
                    'Cover with a clean, dry cloth'
                ]
        
        return guidance
    
    def find_nearby_hospitals(
        self, 
        latitude: float, 
        longitude: float, 
        max_results: int = 5,
        max_distance_km: float = 50.0
    ) -> List[Dict]:
        """
        Find nearby hospitals based on coordinates.
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            max_results: Maximum number of results to return
            max_distance_km: Maximum distance in kilometers
            
        Returns:
            List of nearby hospitals sorted by distance
        """
        hospitals_with_distance = []
        
        for hospital in self.hospitals_database:
            distance = self._calculate_distance(
                latitude, longitude,
                hospital['lat'], hospital['lon']
            )
            
            if distance <= max_distance_km:
                hospital_info = hospital.copy()
                hospital_info['distance_km'] = round(distance, 2)
                hospitals_with_distance.append(hospital_info)
        
        # Sort by distance
        hospitals_with_distance.sort(key=lambda x: x['distance_km'])
        
        # Return top results
        return hospitals_with_distance[:max_results]
    
    def find_nearby_pharmacies(
        self, 
        latitude: float, 
        longitude: float, 
        max_results: int = 5,
        max_distance_km: float = 50.0
    ) -> List[Dict]:
        """
        Find nearby 24/7 pharmacies based on coordinates.
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            max_results: Maximum number of results to return
            max_distance_km: Maximum distance in kilometers
            
        Returns:
            List of nearby pharmacies sorted by distance
        """
        pharmacies_with_distance = []
        
        for pharmacy in self.pharmacies_database:
            # Only include 24/7 pharmacies
            if not pharmacy.get('open_24_7'):
                continue
                
            distance = self._calculate_distance(
                latitude, longitude,
                pharmacy['lat'], pharmacy['lon']
            )
            
            if distance <= max_distance_km:
                pharmacy_info = pharmacy.copy()
                pharmacy_info['distance_km'] = round(distance, 2)
                pharmacies_with_distance.append(pharmacy_info)
        
        # Sort by distance
        pharmacies_with_distance.sort(key=lambda x: x['distance_km'])
        
        # Return top results
        return pharmacies_with_distance[:max_results]
    
    def _calculate_distance(
        self, 
        lat1: float, 
        lon1: float, 
        lat2: float, 
        lon2: float
    ) -> float:
        """
        Calculate distance between two coordinates using Haversine formula.
        
        Returns:
            Distance in kilometers
        """
        # Earth's radius in kilometers
        R = 6371.0
        
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        distance = R * c
        return distance
    
    def get_hospital_by_city(self, city: str) -> List[Dict]:
        """
        Get hospitals in a specific city.
        
        Args:
            city: City name
            
        Returns:
            List of hospitals in the city
        """
        city_lower = city.lower()
        matching_hospitals = []
        
        for hospital in self.hospitals_database:
            if city_lower in hospital['address'].lower():
                matching_hospitals.append(hospital)
        
        return matching_hospitals
    
    def format_hospital_info(self, hospital: Dict) -> str:
        """Format hospital information for display."""
        info_parts = [
            f"🏥 **{hospital['name']}**",
            f"📍 {hospital['address']}",
            f"📞 {hospital['phone']}",
            f"🏛️ Type: {hospital['type']}"
        ]
        
        if 'distance_km' in hospital:
            info_parts.append(f"📏 Distance: {hospital['distance_km']} km")
        
        if hospital.get('emergency'):
            info_parts.append("🚨 24/7 Emergency Services Available")
        
        return '\n'.join(info_parts)


# Singleton instance
_emergency_support_instance = None

def get_emergency_support() -> EmergencySupport:
    """Get or create emergency support instance."""
    global _emergency_support_instance
    if _emergency_support_instance is None:
        _emergency_support_instance = EmergencySupport()
    return _emergency_support_instance
