"""
Geocoding utilities using Google Maps API
"""
import httpx
from typing import Optional

from app.config import settings


async def get_address_from_coordinates(lat: float, lng: float) -> Optional[str]:
    """
    Get address from latitude and longitude using Google Maps Geocoding API.
    
    Args:
        lat: Latitude
        lng: Longitude
        
    Returns:
        str: Formatted address or None if not found
    """
    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "latlng": f"{lat},{lng}",
            "key": settings.GOOGLE_MAPS_API_KEY,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data["status"] == "OK" and data["results"]:
                return data["results"][0]["formatted_address"]
            
            return None
            
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None