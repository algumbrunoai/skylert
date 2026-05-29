import requests

# =========================================================
# TRADUÇÃO DOS CÓDIGOS CLIMÁTICOS
# =========================================================

TRADUCAO_CLIMA = {
    0: "Céu Limpo / Ensolarado",
    1: "Principalmente Limpo",
    2: "Parcialmente Nublado",
    3: "Nublado",
    45: "Névoa",
    48: "Neblina",
    51: "Chuvisco Leve",
    53: "Chuvisco",
    55: "Chuvisco Forte",
    61: "Chuva Leve",
    63: "Chuva",
    65: "Chuva Forte",
    80: "Pancadas de Chuva",
    95: "Tempestade"
}

# =========================================================
# GERA ID PADRONIZADO DA CIDADE
# =========================================================

def gerar_id_cidade(cidade):

    return (
        cidade
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )

# =========================================================
# GEOCODING
# =========================================================

def obter_coordenadas(cidade):

    geo_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
    )

    params = {
        "name": cidade,
        "count": 1,
        "language": "pt",
        "format": "json"
    }

    response = requests.get(
        geo_url,
        params=params,
        timeout=10
    )

    dados = response.json()

    if "results" not in dados:
        return None

    resultado = dados["results"][0]

    return {
        "latitude": resultado["latitude"],
        "longitude": resultado["longitude"],
        "nome": resultado["name"]
    }

# =========================================================
# CONSULTA OPEN-METEO
# =========================================================

def obter_clima(cidade):

    coordenadas = obter_coordenadas(cidade)

    if not coordenadas:
        return None

    latitude = coordenadas["latitude"]
    longitude = coordenadas["longitude"]

    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
    )

    params = {

        "latitude": latitude,
        "longitude": longitude,

        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "precipitation_probability",
            "weather_code",
            "wind_speed_10m",
            "is_day"
        ],

        "timezone": "America/Sao_Paulo"
    }

    response = requests.get(
        weather_url,
        params=params,
        timeout=10
    )

    dados = response.json()

    current = dados.get("current")

    if not current:
        return None

    codigo = current.get("weather_code", 0)

    return {

        "cidade": cidade,

        "weather_code": codigo,

        "descricao": TRADUCAO_CLIMA.get(
            codigo,
            "Desconhecido"
        ),

        "temperatura":
            current.get("temperature_2m"),

        "sensacao":
            current.get("apparent_temperature"),

        "umidade":
            current.get("relative_humidity_2m"),

        "vento":
            current.get("wind_speed_10m"),

        "precipitacao":
            current.get("precipitation"),

        "chuva":
            current.get(
                "precipitation_probability"
            ),

        "is_day":
            current.get("is_day")
    }
if __name__ == "__main__":
    clima = obter_clima("Manaus")
        
    print(clima)