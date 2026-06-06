from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)

# Libera CORS APENAS para os seus ambientes seguros
ORIGENS_PERMITIDAS = [
    "http://127.0.0.1:5500",  # Típico do Live Server do VSCode
    "http://localhost:5500",
    "http://127.0.0.1:5000",
    "http://localhost:5000",
    "https://skylert.vercel.app"     # Quando for publicar, coloque seu domínio real aqui
]

# Libera CORS para o frontend
CORS(app, resources={r"/api/*": {"origins": ORIGENS_PERMITIDAS}})

# =========================================================
# TRADUÇÃO DOS CÓDIGOS DE CLIMA
# =========================================================

TRADUCAO_CLIMA = {
    0: "Céu Limpo",
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
    95: "Tempestade",
}


# =========================================================
# API DE PREVISÃO
# =========================================================


@app.route("/api/previsao", methods=["GET"])
def obter_previsao():

    cidade = request.args.get("cidade", "Sao Paulo")

    # Coordenadas opcionais
    latitude_param = request.args.get("lat")
    longitude_param = request.args.get("lon")

    try:

        # ==========================================
        # BUSCA COORDENADAS
        # ==========================================

        if latitude_param and longitude_param:

            latitude = float(latitude_param)
            longitude = float(longitude_param)

            nome_cidade = cidade

        else:

            geo_url = "https://geocoding-api.open-meteo.com/v1/search"

            geo_params = {
                "name": cidade,
                "count": 1,
                "language": "pt",
                "format": "json",
            }

            geo_response = requests.get(geo_url, params=geo_params, timeout=10)

            geo_data = geo_response.json()

            if "results" not in geo_data:
                return jsonify({"erro": "Cidade não encontrada"}), 404

            resultado = geo_data["results"][0]

            latitude = resultado["latitude"]
            longitude = resultado["longitude"]

            estado = resultado.get("admin1", "")

            nome_cidade = f"{resultado['name']} - {estado}"

        # ==========================================
        # BUSCA PREVISÃO DO TEMPO
        # ==========================================

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation_probability",
                "precipitation",
                "weather_code",
                "wind_speed_10m",
                "is_day",
            ],
            "daily": ["temperature_2m_max", "temperature_2m_min"],
            "timezone": "auto",
            "forecast_days": 16,
        }

        weather_response = requests.get(weather_url, params=weather_params, timeout=10)

        dados = weather_response.json()

        # ==========================================
        # DADOS ATUAIS
        # ==========================================

        current = dados["current"]

        codigo_clima = current.get("weather_code", 0)

        # ==========================================
        # PREVISÃO DOS PRÓXIMOS 3 DIAS
        # ==========================================

        previsao_diaria = []

        datas = dados["daily"]["time"]
        maximas = dados["daily"]["temperature_2m_max"]
        minimas = dados["daily"]["temperature_2m_min"]

        hoje = datetime.now().date()

        for i in range(len(datas)):

            data_obj = datetime.strptime(datas[i], "%Y-%m-%d").date()

            # Ignora o dia atual
            if data_obj <= hoje:
                continue

            previsao_diaria.append(
                {
                    "data": data_obj.strftime("%d/%m/%Y"),
                    "max": round(maximas[i]),
                    "min": round(minimas[i]),
                }
            )

            # Limita a 3 dias
            if len(previsao_diaria) == 3:
                break

        # ==========================================
        # RESPOSTA FINAL
        # ==========================================

        resposta = {
            "cidade_nome": nome_cidade,
            "temp_atual": round(current.get("temperature_2m", 0)),
            "sensacao": round(current.get("apparent_temperature", 0)),
            "condicao": TRADUCAO_CLIMA.get(codigo_clima, "Desconhecido"),
            "codigo_clima": codigo_clima,
            "is_day": current.get("is_day", 1),
            "precipitacao_atual": current.get("precipitation", 0),
            "vento": round(current.get("wind_speed_10m", 0), 1),
            "umidade": current.get("relative_humidity_2m", 0),
            "uv": 0,
            "chuva": current.get("precipitation_probability", 0),
            "previsao_dias": previsao_diaria,
        }

        return jsonify(resposta), 200

    except Exception as e:

        print(e)

        return jsonify({"erro": str(e)}), 500


# =========================================================
# API DE AUTOCOMPLETE DE CIDADES
# =========================================================


@app.route("/api/cidades", methods=["GET"])
def buscar_cidades():

    termo = request.args.get("q", "")

    if len(termo) < 2:
        return jsonify([])

    try:

        url = "https://geocoding-api.open-meteo.com/v1/search"

        params = {"name": termo, "count": 5, "language": "pt", "format": "json"}

        response = requests.get(url, params=params, timeout=10)

        dados = response.json()

        cidades = []

        if "results" in dados:

            for cidade in dados["results"]:

                nome = cidade.get("name", "")
                estado = cidade.get("admin1", "")

                cidades.append(
                    {
                        "nome": f"{nome} - {estado}",
                        "latitude": cidade.get("latitude"),
                        "longitude": cidade.get("longitude"),
                    }
                )

        return jsonify(cidades)

    except Exception as e:

        print(e)

        return jsonify({"erro": str(e)}), 500


# =========================================================
# INICIAR SERVIDOR
# =========================================================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
