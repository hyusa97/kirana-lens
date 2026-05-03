"""
Geographic analysis service using Google Maps APIs and OpenStreetMap Nominatim
"""
import asyncio
from typing import Dict, List

import httpx
from fastapi import HTTPException, status

from app.config import settings


class GeoService:
    """Service for analyzing geographic and location-based features"""
    
    def __init__(self):
        self.google_api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
        self.use_nominatim = getattr(settings, 'USE_NOMINATIM', False)
        self.timeout = 30.0
        
        # Nominatim API endpoint
        self.nominatim_base_url = "https://nominatim.openstreetmap.org"
        
        # User agent for Nominatim (required by their usage policy)
        self.nominatim_headers = {
            "User-Agent": "KiranaLens/1.0 (credit-assessment-app)"
        }
    
    async def analyze_location(self, lat: float, lng: float) -> Dict:
        """
        Analyze location to extract geographic features for credit assessment.
        
        Args:
            lat: Latitude coordinate
            lng: Longitude coordinate
            
        Returns:
            Dict: Geographic analysis results with all 5 scores and raw data
            
        Raises:
            HTTPException: If analysis fails
        """
        try:
            if self.use_nominatim:
                return await self._analyze_location_nominatim(lat, lng)
            else:
                return await self._analyze_location_google(lat, lng)
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Geographic analysis failed: {str(e)}"
            )
    
    async def _analyze_location_nominatim(self, lat: float, lng: float) -> Dict:
        """Analyze location using OpenStreetMap Nominatim (FREE)"""
        try:
            # Run all geographic analyses concurrently using Nominatim
            results = await asyncio.gather(
                self._analyze_road_type_nominatim(lat, lng),
                self._analyze_competition_density_nominatim(lat, lng),
                self._analyze_footfall_proxy_nominatim(lat, lng),
                self._analyze_catchment_density_nominatim(lat, lng),
                self._analyze_neighbourhood_quality_nominatim(lat, lng),
                return_exceptions=True
            )
            
            # Check for exceptions
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    analysis_names = [
                        "road_type", "competition_density", "footfall_proxy",
                        "catchment_density", "neighbourhood_quality"
                    ]
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Failed to analyze {analysis_names[i]}: {str(result)}"
                    )
            
            # Combine all results
            road_data, competition_data, footfall_data, catchment_data, neighbourhood_data = results
            
            return {
                "road_type_score": road_data["score"],
                "catchment_density_score": catchment_data["score"],
                "footfall_proxy_index": footfall_data["score"],
                "competition_density_score": competition_data["score"],
                "neighbourhood_quality_score": neighbourhood_data["score"],
                "competitor_count": competition_data["competitor_count"],
                "poi_count": footfall_data["poi_count"],
                "provider": "nominatim",
                "raw_nominatim_response": {
                    "competition": competition_data["raw_response"],
                    "catchment": catchment_data["raw_response"],
                    "neighbourhood": neighbourhood_data["raw_response"],
                    "footfall": footfall_data["raw_response"],
                    "roads": road_data["raw_response"]
                }
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Nominatim geographic analysis failed: {str(e)}"
            )
    
    async def _analyze_location_google(self, lat: float, lng: float) -> Dict:
        """Analyze location using Google Maps APIs (original implementation)"""
        # Run all geographic analyses concurrently
        results = await asyncio.gather(
            self._analyze_road_type(lat, lng),
            self._analyze_competition_density(lat, lng),
            self._analyze_footfall_proxy(lat, lng),
            self._analyze_catchment_density(lat, lng),
            self._analyze_neighbourhood_quality(lat, lng),
            return_exceptions=True
        )
        
        # Check for exceptions
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                analysis_names = [
                    "road_type", "competition_density", "footfall_proxy",
                    "catchment_density", "neighbourhood_quality"
                ]
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to analyze {analysis_names[i]}: {str(result)}"
                )
        
        # Combine all results
        road_data, competition_data, footfall_data, catchment_data, neighbourhood_data = results
        
        return {
            "road_type_score": road_data["score"],
            "catchment_density_score": catchment_data["score"],
            "footfall_proxy_index": footfall_data["score"],
            "competition_density_score": competition_data["score"],
            "neighbourhood_quality_score": neighbourhood_data["score"],
            "competitor_count": competition_data["competitor_count"],
            "poi_count": footfall_data["poi_count"],
            "provider": "google",
            "raw_places_response": {
                "competition": competition_data["raw_response"],
                "catchment": catchment_data["raw_response"],
                "neighbourhood": neighbourhood_data["raw_response"]
            },
            "raw_overpass_response": footfall_data["raw_response"],
            "raw_roads_response": road_data["raw_response"]
        }
    
    # Nominatim-based analysis methods
    async def _analyze_road_type_nominatim(self, lat: float, lng: float) -> Dict:
        """Analyze road type using Nominatim reverse geocoding."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout, headers=self.nominatim_headers) as client:
                # Use reverse geocoding to get road information
                url = f"{self.nominatim_base_url}/reverse"
                params = {
                    "lat": lat,
                    "lon": lng,
                    "format": "json",
                    "addressdetails": 1,
                    "extratags": 1
                }
                
                # Add delay to respect rate limits (1 request per second)
                await asyncio.sleep(1)
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Analyze road type from address details
                score = self._calculate_road_score_nominatim(data)
                
                return {
                    "score": score,
                    "raw_response": data
                }
                
        except Exception as e:
            return {
                "score": 50,
                "raw_response": {"error": f"Road analysis failed: {str(e)}"}
            }
    
    async def _analyze_competition_density_nominatim(self, lat: float, lng: float) -> Dict:
        """Analyze competition using Overpass API for grocery stores."""
        try:
            # Build Overpass query for grocery stores within 500m
            overpass_query = f"""
            [out:json][timeout:25];
            (
              node["shop"~"^(supermarket|convenience|grocery|general)$"](around:500,{lat},{lng});
              way["shop"~"^(supermarket|convenience|grocery|general)$"](around:500,{lat},{lng});
            );
            out center;
            """
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = "https://overpass-api.de/api/interpreter"
                
                # Add delay to respect rate limits
                await asyncio.sleep(1)
                
                response = await client.post(url, data=overpass_query)
                response.raise_for_status()
                data = response.json()
                
                # Count competitors
                competitors = data.get("elements", [])
                competitor_count = len(competitors)
                
                # Calculate competition density score
                # Higher competition = lower score (more challenging environment)
                score = max(0, 100 - (competitor_count * 15))
                
                return {
                    "score": score,
                    "competitor_count": competitor_count,
                    "raw_response": data
                }
                
        except Exception as e:
            return {
                "score": 50,
                "competitor_count": 0,
                "raw_response": {"error": f"Competition analysis failed: {str(e)}"}
            }
    
    async def _analyze_footfall_proxy_nominatim(self, lat: float, lng: float) -> Dict:
        """Analyze footfall proxy using Overpass API for POIs."""
        try:
            # Build Overpass query for relevant POIs within 300m
            overpass_query = f"""
            [out:json][timeout:25];
            (
              node["amenity"~"^(school|college|university|hospital|clinic|bus_station|railway_station|office|bank|fuel|restaurant|cafe)$"](around:300,{lat},{lng});
              node["shop"~"^(supermarket|mall|department_store)$"](around:300,{lat},{lng});
              way["amenity"~"^(school|college|university|hospital|clinic|bus_station|railway_station|office|bank|fuel|restaurant|cafe)$"](around:300,{lat},{lng});
              way["shop"~"^(supermarket|mall|department_store)$"](around:300,{lat},{lng});
            );
            out center;
            """
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = "https://overpass-api.de/api/interpreter"
                
                # Add delay to respect rate limits
                await asyncio.sleep(1)
                
                response = await client.post(url, data=overpass_query)
                response.raise_for_status()
                data = response.json()
                
                # Count POIs
                poi_count = len(data.get("elements", []))
                
                # Calculate footfall proxy index
                # More POIs = higher footfall potential
                score = min(100, poi_count * 8)  # Slightly lower multiplier than Google
                
                return {
                    "score": score,
                    "poi_count": poi_count,
                    "raw_response": data
                }
                
        except Exception as e:
            return {
                "score": 50,
                "poi_count": 0,
                "raw_response": {"error": f"Footfall analysis failed: {str(e)}"}
            }
    
    async def _analyze_catchment_density_nominatim(self, lat: float, lng: float) -> Dict:
        """Analyze catchment density using Overpass API."""
        try:
            # Build Overpass query for residential and commercial areas
            overpass_query = f"""
            [out:json][timeout:25];
            (
              node["building"~"^(residential|house|apartments|commercial|office|retail)$"](around:500,{lat},{lng});
              way["building"~"^(residential|house|apartments|commercial|office|retail)$"](around:500,{lat},{lng});
              node["landuse"~"^(residential|commercial)$"](around:500,{lat},{lng});
              way["landuse"~"^(residential|commercial)$"](around:500,{lat},{lng});
            );
            out center;
            """
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = "https://overpass-api.de/api/interpreter"
                
                # Add delay to respect rate limits
                await asyncio.sleep(1)
                
                response = await client.post(url, data=overpass_query)
                response.raise_for_status()
                data = response.json()
                
                # Count residential vs commercial buildings
                elements = data.get("elements", [])
                residential_count = 0
                commercial_count = 0
                
                for element in elements:
                    tags = element.get("tags", {})
                    building_type = tags.get("building", "")
                    landuse_type = tags.get("landuse", "")
                    
                    if building_type in ["residential", "house", "apartments"] or landuse_type == "residential":
                        residential_count += 1
                    elif building_type in ["commercial", "office", "retail"] or landuse_type == "commercial":
                        commercial_count += 1
                
                # Calculate catchment density score
                total_buildings = residential_count + commercial_count
                if total_buildings > 0:
                    residential_ratio = residential_count / total_buildings
                    score = int(residential_ratio * 100)
                else:
                    score = 50  # Neutral score if no data
                
                return {
                    "score": score,
                    "raw_response": {
                        "elements": data,
                        "residential_count": residential_count,
                        "commercial_count": commercial_count
                    }
                }
                
        except Exception as e:
            return {
                "score": 50,
                "raw_response": {"error": f"Catchment analysis failed: {str(e)}"}
            }
    
    async def _analyze_neighbourhood_quality_nominatim(self, lat: float, lng: float) -> Dict:
        """Analyze neighbourhood quality using Nominatim address details."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout, headers=self.nominatim_headers) as client:
                # Use reverse geocoding to get detailed address information
                url = f"{self.nominatim_base_url}/reverse"
                params = {
                    "lat": lat,
                    "lon": lng,
                    "format": "json",
                    "addressdetails": 1,
                    "extratags": 1,
                    "namedetails": 1
                }
                
                # Add delay to respect rate limits
                await asyncio.sleep(1)
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Calculate neighbourhood quality score based on address details
                score = self._calculate_neighbourhood_score_nominatim(data)
                
                return {
                    "score": score,
                    "raw_response": data
                }
                
        except Exception as e:
            return {
                "score": 50,
                "raw_response": {"error": f"Neighbourhood analysis failed: {str(e)}"}
            }
    
    def _calculate_road_score_nominatim(self, data: Dict) -> int:
        """Calculate road type score from Nominatim response."""
        try:
            address = data.get("address", {})
            road = address.get("road", "")
            road_type = address.get("highway", "")
            
            # Score based on road presence and type
            if not road:
                return 30  # Low score if no road identified
            
            # Basic scoring based on road type (if available)
            if road_type in ["primary", "trunk", "motorway"]:
                return 85  # Major roads
            elif road_type in ["secondary", "tertiary"]:
                return 70  # Medium roads
            elif road_type in ["residential", "service"]:
                return 55  # Local roads
            else:
                return 60  # Default for roads with data
                
        except Exception:
            return 50  # Neutral score on error
    
    def _calculate_neighbourhood_score_nominatim(self, data: Dict) -> int:
        """Calculate neighbourhood quality score from Nominatim response."""
        try:
            address = data.get("address", {})
            
            # Score based on address completeness and area type
            score = 50  # Base score
            
            # Bonus for complete address information
            if address.get("house_number"):
                score += 10
            if address.get("postcode"):
                score += 10
            if address.get("city") or address.get("town"):
                score += 10
            if address.get("state"):
                score += 5
            
            # Bonus for urban areas (typically better infrastructure)
            place_type = data.get("type", "")
            if place_type in ["city", "town", "suburb"]:
                score += 15
            elif place_type in ["village", "hamlet"]:
                score += 5
            
            return min(100, score)
            
        except Exception:
            return 50  # Neutral score on error
    
    async def _analyze_road_type(self, lat: float, lng: float) -> Dict:
        """Analyze road type using Google Roads API."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Use Google Roads API to get nearest roads
                url = "https://roads.googleapis.com/v1/nearestRoads"
                params = {
                    "points": f"{lat},{lng}",
                    "key": self.google_api_key
                }
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Analyze road type and assign score
                score = self._calculate_road_type_score(data)
                
                return {
                    "score": score,
                    "raw_response": data
                }
                
        except Exception as e:
            # Fallback: use Places API to get nearby roads
            return await self._fallback_road_analysis(lat, lng)
    
    async def _fallback_road_analysis(self, lat: float, lng: float) -> Dict:
        """Fallback road analysis using Places API."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                params = {
                    "location": f"{lat},{lng}",
                    "radius": 100,
                    "type": "route",
                    "key": self.google_api_key
                }
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Default scoring based on location context
                score = 50  # Neutral score when road data unavailable
                
                return {
                    "score": score,
                    "raw_response": data
                }
                
        except Exception:
            # Ultimate fallback
            return {
                "score": 50,
                "raw_response": {"error": "Road analysis unavailable"}
            }
    
    async def _analyze_competition_density(self, lat: float, lng: float) -> Dict:
        """Analyze competition density using Google Places API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            params = {
                "location": f"{lat},{lng}",
                "radius": 500,
                "type": "grocery_or_supermarket",
                "key": self.google_api_key
            }
            
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Count competitors (excluding the store itself)
            competitors = data.get("results", [])
            competitor_count = len(competitors)
            
            # Calculate competition density score
            # Higher competition = lower score (more challenging environment)
            score = max(0, 100 - (competitor_count * 15))
            
            return {
                "score": score,
                "competitor_count": competitor_count,
                "raw_response": data
            }
    
    async def _analyze_footfall_proxy(self, lat: float, lng: float) -> Dict:
        """Analyze footfall proxy using Overpass API for POIs."""
        try:
            # Build Overpass query for relevant POIs within 300m
            overpass_query = f"""
            [out:json][timeout:25];
            (
              node["amenity"~"^(school|college|hospital|bus_station|railway_station|office|bank|fuel)$"](around:300,{lat},{lng});
              node["shop"~"^(supermarket|mall)$"](around:300,{lat},{lng});
            );
            out geom;
            """
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = "https://overpass-api.de/api/interpreter"
                response = await client.post(url, data=overpass_query)
                response.raise_for_status()
                data = response.json()
                
                # Count POIs
                poi_count = len(data.get("elements", []))
                
                # Calculate footfall proxy index
                # More POIs = higher footfall potential
                score = min(100, poi_count * 12)
                
                return {
                    "score": score,
                    "poi_count": poi_count,
                    "raw_response": data
                }
                
        except Exception as e:
            # Fallback to Google Places for POI analysis
            return await self._fallback_footfall_analysis(lat, lng)
    
    async def _fallback_footfall_analysis(self, lat: float, lng: float) -> Dict:
        """Fallback footfall analysis using Google Places."""
        try:
            poi_types = ["school", "hospital", "bank", "bus_station", "shopping_mall"]
            total_pois = 0
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                for poi_type in poi_types:
                    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        "location": f"{lat},{lng}",
                        "radius": 300,
                        "type": poi_type,
                        "key": self.google_api_key
                    }
                    
                    response = await client.get(url, params=params)
                    if response.status_code == 200:
                        data = response.json()
                        total_pois += len(data.get("results", []))
            
            score = min(100, total_pois * 12)
            
            return {
                "score": score,
                "poi_count": total_pois,
                "raw_response": {"poi_count": total_pois, "method": "google_places_fallback"}
            }
            
        except Exception:
            return {
                "score": 50,
                "poi_count": 0,
                "raw_response": {"error": "Footfall analysis unavailable"}
            }
    
    async def _analyze_catchment_density(self, lat: float, lng: float) -> Dict:
        """Analyze catchment density using Google Places API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Search for residential and commercial areas
            residential_params = {
                "location": f"{lat},{lng}",
                "radius": 500,
                "type": "neighborhood",
                "key": self.google_api_key
            }
            
            commercial_params = {
                "location": f"{lat},{lng}",
                "radius": 500,
                "type": "establishment",
                "key": self.google_api_key
            }
            
            # Make both requests
            residential_response = await client.get(
                "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
                params=residential_params
            )
            commercial_response = await client.get(
                "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
                params=commercial_params
            )
            
            residential_data = residential_response.json() if residential_response.status_code == 200 else {}
            commercial_data = commercial_response.json() if commercial_response.status_code == 200 else {}
            
            # Count residential vs commercial establishments
            residential_count = len(residential_data.get("results", []))
            commercial_count = len(commercial_data.get("results", []))
            
            # Calculate catchment density score
            # Higher residential density = better catchment
            total_establishments = residential_count + commercial_count
            if total_establishments > 0:
                residential_ratio = residential_count / total_establishments
                score = int(residential_ratio * 100)
            else:
                score = 50  # Neutral score if no data
            
            return {
                "score": score,
                "raw_response": {
                    "residential": residential_data,
                    "commercial": commercial_data,
                    "residential_count": residential_count,
                    "commercial_count": commercial_count
                }
            }
    
    async def _analyze_neighbourhood_quality(self, lat: float, lng: float) -> Dict:
        """Analyze neighbourhood quality using Google Places ratings."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            params = {
                "location": f"{lat},{lng}",
                "radius": 200,
                "key": self.google_api_key
            }
            
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Calculate average rating of nearby places
            places = data.get("results", [])
            ratings = [place.get("rating", 0) for place in places if place.get("rating")]
            
            if ratings:
                avg_rating = sum(ratings) / len(ratings)
                # Convert 5-star rating to 100-point scale
                score = int((avg_rating / 5.0) * 100)
            else:
                score = 50  # Neutral score if no ratings available
            
            return {
                "score": score,
                "raw_response": data
            }
    
    def _calculate_road_type_score(self, roads_data: Dict) -> int:
        """Calculate road type score from Google Roads API response."""
        try:
            snapped_points = roads_data.get("snappedPoints", [])
            if not snapped_points:
                return 50  # Neutral score if no road data
            
            # Analyze road characteristics
            # This is a simplified scoring - in production, you'd analyze
            # speed limits, road classifications, etc.
            
            # For now, assume presence of road data indicates decent accessibility
            return 65  # Above average score for roads with data
            
        except Exception:
            return 50  # Neutral score on error