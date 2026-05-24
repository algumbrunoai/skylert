import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Busca a chave de forma segura
TOMORROW_API_KEY = os.getenv("TOMORROW_API_KEY")

TRADUCAO_CLIMA = {
    1000: "Céu Limpo / Ensolarado",
    1100: "Majoritariamente Limpo",
    1101: "Parcialmente Nublado",
    1102: "Majoritariamente Nublado",
    1001: "Nublado",
    2000: "Névoa",
    2100: "Neblina leve",
    4000: "Chuvisco",
    4001: "Chuva",
    4200: "Chuva Leve",
    4201: "Chuva Forte",
    8000: "Tempestade"
}

@app.route('/api/previsao', methods=['GET'])
def obter_previsao():
    cidade = request.args.get('cidade', 'Sao Paulo')
    url = "https://api.tomorrow.io/v4/weather/forecast"
    
    params = {
        "location": cidade,
        "apikey": TOMORROW_API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            dados = response.json()
            
            # Pega dados atuais (primeira hora)
            atual_valores = dados['timelines']['hourly'][0]['values']
            codigo_clima = atual_valores.get('weatherCode', 1000)
            
            # Conversão do vento de m/s para km/h (multiplica por 3.6)
            vento_ms = atual_valores.get('windSpeed', 0)
            vento_kmh = round(vento_ms * 3.6, 1)
            
            # Previsão dos próximos 3 dias
            previsao_diaria = []
            for dia in dados['timelines']['daily'][:3]:
                previsao_diaria.append({
                    "data": dia['time'].split('T')[0],
                    "min": round(dia['values']['temperatureMin']),
                    "max": round(dia['values']['temperatureMax'])
                })
            
            # Limpa o nome da cidade removendo o excesso geográfico
            nome_cidade_limpo = dados['location']['name'].split(',')[0].strip()
            
            resposta_simplificada = {
                "cidade_nome": nome_cidade_limpo,
                "temp_atual": round(atual_valores.get('temperature', 0)),
                "sensacao": round(atual_valores.get('temperatureApparent', 0)),
                "condicao": TRADUCAO_CLIMA.get(codigo_clima, "Desconhecido"),
                "vento": vento_kmh,
                "umidade": atual_valores.get('humidity', 0),
                "uv": atual_valores.get('uvIndex', 0),
                "chuva": atual_valores.get('precipitationProbability', 0),
                "previsao_dias": previsao_diaria
            }
            
            return jsonify(resposta_simplificada), 200
        else:
            return jsonify({"erro": "Erro na API da Tomorrow.io"}), response.status_code
            
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)