import requests

def get_lat_lon(address):
    """住所から緯度経度を取得（Nominatim使用）"""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
        "countrycodes": "jp",
    }
    headers = {
        "User-Agent": "FarmWeatherApp/1.0"
    }
    res = requests.get(url, params=params, headers=headers)
    data = res.json()
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    return None, None

def get_weather(lat, lon, api_key):
    """OpenWeatherMapから天気取得"""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",
        "lang": "ja",
    }
    res = requests.get(url, params=params)
    return res.json()

def try_address_with_backoff(address, min_length=5, max_attempts=10):
    """
    住所を末尾から削っていき、Nominatimが解釈できるまで試す。
    """
    for i in range(max_attempts):
        attempt = address[:len(address)-i].strip()
        if len(attempt) < min_length:
            break  # 短すぎる場合は諦める
        lat, lon = get_lat_lon(attempt)
        if lat and lon:
            return lat, lon
    return None, None