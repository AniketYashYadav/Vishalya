import logging
import httpx
from typing import Optional, Tuple
from backend.core import config

logger = logging.getLogger("vishalya.weather")

# OpenWeather Air Pollution Index (1-5) mapping to standard US AQI scale range
AQI_INDEX_MAP = {
    1: 40.0,   # Good (0 - 50)
    2: 80.0,   # Fair (51 - 100)
    3: 130.0,  # Moderate (101 - 150)
    4: 180.0,  # Poor (151 - 200)
    5: 320.0,  # Very Poor (201 - 500)
}


def calculate_aqi_from_components(components: dict) -> float:
    """
    Calculates standard AQI value from particulate matter concentrations (PM2.5 / PM10).
    """
    pm2_5 = components.get("pm2_5", 0.0)
    pm10 = components.get("pm10", 0.0)
    
    # Standard EPA PM2.5 to AQI calculation approximation
    if pm2_5 > 0:
        if pm2_5 <= 12.0:
            return round((50.0 / 12.0) * pm2_5, 1)
        elif pm2_5 <= 35.4:
            return round(50.0 + ((50.0 / 23.4) * (pm2_5 - 12.0)), 1)
        elif pm2_5 <= 55.4:
            return round(100.0 + ((50.0 / 20.0) * (pm2_5 - 35.4)), 1)
        elif pm2_5 <= 150.4:
            return round(150.0 + ((50.0 / 95.0) * (pm2_5 - 55.4)), 1)
        else:
            return round(200.0 + ((100.0 / 99.6) * (pm2_5 - 150.4)), 1)

    if pm10 > 0:
        return round(min(pm10 * 2.0, 500.0), 1)

    return config.FALLBACK_AQI


async def fetch_coordinates_by_pin(village_pin: str, country_code: str = "IN") -> Optional[Tuple[float, float]]:
    """
    Resolves postal PIN code to (lat, lon) coordinates using OpenWeather Geocoding API.
    """
    if not config.OPENWEATHER_API_KEY:
        return None

    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(
                config.OPENWEATHER_GEO_URL,
                params={"zip": f"{village_pin},{country_code}", "appid": config.OPENWEATHER_API_KEY}
            )
            if resp.status_code == 200:
                data = resp.json()
                return float(data["lat"]), float(data["lon"])
    except Exception as err:
        logger.warning(f"Geocoding lookup failed for PIN {village_pin}: {err}")

    return None


async def get_live_aqi(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    village_pin: Optional[str] = None
) -> Tuple[float, str]:
    """
    Fetches live AQI using GPS coordinates or village postal PIN code.
    Returns tuple of (aqi_value, source_name).
    """
    # 1. Resolve coordinates if missing but village_pin provided
    if (latitude is None or longitude is None) and village_pin:
        coords = await fetch_coordinates_by_pin(village_pin)
        if coords:
            latitude, longitude = coords

    # 2. Query OpenWeather Pollution API if credentials and coordinates are available
    if config.OPENWEATHER_API_KEY and latitude is not None and longitude is not None:
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.get(
                    config.OPENWEATHER_AQI_URL,
                    params={
                        "lat": latitude,
                        "lon": longitude,
                        "appid": config.OPENWEATHER_API_KEY
                    }
                )
                if resp.status_code == 200:
                    payload = resp.json()
                    list_data = payload.get("list", [])
                    if list_data:
                        item = list_data[0]
                        components = item.get("components", {})
                        main_aqi_index = item.get("main", {}).get("aqi")
                        
                        # Priority 1: Compute fine-grained AQI from PM2.5/PM10 components
                        computed_aqi = calculate_aqi_from_components(components)
                        if computed_aqi > 0:
                            return computed_aqi, "live_openweathermap"

                        # Priority 2: Use mapped index level
                        if main_aqi_index in AQI_INDEX_MAP:
                            return AQI_INDEX_MAP[main_aqi_index], "live_openweathermap"
        except Exception as err:
            logger.warning(f"OpenWeather API request failed: {err}")

    # 3. Fallback when API key is unconfigured or request times out
    return config.FALLBACK_AQI, "fallback_default"
