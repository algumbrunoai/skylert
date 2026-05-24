import os
import firebase_admin
from firebase_admin import credentials, firestore
import requests
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do .env
load_dotenv()

# Inicialização do Firebase
cred = credentials.Certificate("firebase-chave.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Busca as credenciais de forma segura do .env
TOMORROW_API_KEY = os.getenv("TOMORROW_API_KEY")
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA_APP = os.getenv("EMAIL_SENHA_APP")

def enviar_email_alerta(destinatario, cidade, tipo_alerta, mensagem_clima):
    assunto = f"⚠️ ALERTA CLIMÁTICO - Skylert ({cidade})"
    corpo = f"""
    Olá!
    
    O Skylert detectou uma condição climática preocupante na sua região monitorada ({cidade}).
    
    Tipo de ocorrência: {tipo_alerta}
    Detalhes: {mensagem_clima}
    
    Por favor, tome os devidos cuidados.
    Atenciosamente,
    Equipe Skylert.
    """
    
    msg = MIMEText(corpo)
    msg['Subject'] = assunto
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = destinatario

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(EMAIL_REMETENTE, EMAIL_SENHA_APP)
            servidor.sendmail(EMAIL_REMETENTE, destinatario, msg.as_string())
        print(f"E-mail de alerta enviado com sucesso para {destinatario}!")
    except Exception as e:
        print(f"Falha ao enviar e-mail para {destinatario}: {e}")

def verificar_clima_e_alertar():
    print("Iniciando verificação de alertas climáticos...")
    
    usuarios_ref = db.collection("alertas_config")
    docs = usuarios_ref.stream()

    for doc in docs:
        dados = doc.to_dict()
        email_usuario = dados.get('emailUsuario')
        cidade = dados.get('cidadeMonitorada')
        
        if not email_usuario or not cidade:
            continue

        print(f"Verificando clima para {email_usuario} na cidade {cidade}...")
        
        url = "https://api.tomorrow.io/v4/weather/forecast"
        params = {
            "location": cidade,
            "apikey": TOMORROW_API_KEY,
            "units": "metric"
        }
        
        try:
            res = requests.get(url, params=params)
            if res.status_code == 200:
                clima = res.json()
                valores = clima['timelines']['hourly'][0]['values']
                
                chuva_probabilidade = valores.get('precipitationProbability', 0)
                temperatura = valores.get('temperature', 20)
                
                # Conversão de m/s para km/h no vento para consistência
                velocidade_vento_kmh = round(valores.get('windSpeed', 0) * 3.6, 1)
                
                # --- VERIFICAÇÃO DE REGRAS DE ALERTA ---
                # Alerta de Chuva (Modificar para '> 70' quando acabar de fazer os testes locais)
                if dados.get('receberChuva') and chuva_probabilidade >= 0:
                    enviar_email_alerta(
                        email_usuario, 
                        cidade, 
                        "Alta Probabilidade de Chuva Forte", 
                        f"Chance de chuva de {chuva_probabilidade}% detectada para as próximas horas."
                    )
                
                # Alerta de Ventania (Vento acima de 36 km/h)
                if dados.get('receberVento') and velocidade_vento_kmh > 36:
                    enviar_email_alerta(
                        email_usuario, 
                        cidade, 
                        "Ventos Fortes Detectados", 
                        f"Ventos soprando a {velocidade_vento_kmh} km/h na sua região."
                    )
                
                # Alerta de Temperatura Extrema (Abaixo de 12°C ou Acima de 35°C)
                if dados.get('receberTemperatura') and (temperatura < 12 or temperatura > 35):
                    enviar_email_alerta(
                        email_usuario, 
                        cidade, 
                        "Temperatura Extrema", 
                        f"Temperatura crítica registrada de {round(temperatura)}°C."
                    )
            else:
                print(f"Erro ao buscar clima para {cidade}: {res.text}")
                
        except Exception as e:
            print(f"Erro no processamento de {email_usuario}: {e}")

if __name__ == "__main__":
    verificar_clima_e_alertar()