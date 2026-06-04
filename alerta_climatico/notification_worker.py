import os
import smtplib

from firebase_config import db

from dotenv import load_dotenv

from email.mime.text import MIMEText

from skylert_meteo_service import (
    gerar_id_cidade
)

# =========================================================
# ENV
# =========================================================

load_dotenv()

EMAIL_REMETENTE = os.getenv(
    "EMAIL_REMETENTE"
)

EMAIL_SENHA_APP = os.getenv(
    "EMAIL_SENHA_APP"
)

# =========================================================
# ENVIA E-MAIL
# =========================================================

def enviar_email_alerta(
    destinatario,
    cidade,
    titulo,
    mensagem
):

    assunto = (
        f"⚠️ Skylert - {titulo}"
    )

    corpo = f"""
Olá!

O Skylert detectou uma condição climática severa.

Cidade:
{cidade}

Detalhes:
{mensagem}

Tome cuidado.

Equipe Skylert.
"""

    msg = MIMEText(corpo)

    msg['Subject'] = assunto
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = destinatario

    try:

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as servidor:

            servidor.login(
                EMAIL_REMETENTE,
                EMAIL_SENHA_APP
            )

            servidor.sendmail(
                EMAIL_REMETENTE,
                destinatario,
                msg.as_string()
            )

        print(
            f"[OK] E-mail enviado "
            f"para {destinatario}"
        )

    except Exception as e:

        print(
            f"[ERRO] SMTP: {e}"
        )

# =========================================================
# ALERTAS
# =========================================================

def verificar_alertas():

    print("\n==========================")
    print("VERIFICANDO ALERTAS")
    print("==========================\n")

    usuarios = db.collection(
        "alertas_config"
    ).stream()

    for usuario in usuarios:

        try:

            dados = usuario.to_dict()

            cidade = dados.get(
                "cidadeMonitorada"
            )

            email = dados.get(
                "emailUsuario"
            )

            if not cidade or not email:
                continue

            cidade_id = gerar_id_cidade(
                cidade
            )

            clima_doc = db.collection(
                "clima_cache"
            ).document(cidade_id).get()

            if not clima_doc.exists:

                print(
                    f"[ERRO] Cache não "
                    f"encontrado para "
                    f"{cidade}"
                )

                continue

            clima = clima_doc.to_dict()

            codigo = clima.get(
                "weatherCode",
                0
            )

            temperatura = clima.get(
                "temperatura",
                0
            )

            vento = clima.get(
                "vento",
                0
            )

            chuva = clima.get(
                "chuva",
                0
            )

            precipitacao = clima.get(
                "precipitacao",
                0
            )

            descricao = clima.get(
                "descricao",
                "Desconhecido"
            )

            ultimo_codigo = dados.get(
                "ultimoWeatherCode"
            )

            # ======================================
            # EVITA ALERTAS DUPLICADOS
            # ======================================

            if ultimo_codigo == codigo:

                print(
                    f"[INFO] Alerta já "
                    f"enviado para "
                    f"{cidade}"
                )

                continue

            alerta_disparado = False

            # ======================================
            # CHUVA
            # ======================================

            if (
                dados.get("receberChuva")
                and (
                    chuva >= 70
                    or precipitacao > 8
                    or codigo in [65, 80, 95]
                )
            ):

                enviar_email_alerta(

                    email,

                    cidade,

                    "Chuva Forte",

                    (
                        f"{descricao}\n\n"
                        f"Chance de chuva: "
                        f"{chuva}%\n"
                        f"Precipitação: "
                        f"{precipitacao} mm"
                    )
                )

                alerta_disparado = True

            # ======================================
            # VENTO
            # ======================================

            if (
                dados.get("receberVento")
                and vento > 36
            ):

                enviar_email_alerta(

                    email,

                    cidade,

                    "Ventania Extrema",

                    (
                        f"Ventos de "
                        f"{vento} km/h "
                        f"detectados."
                    )
                )

                alerta_disparado = True

            # ======================================
            # TEMPERATURA
            # ======================================

            if (
                dados.get(
                    "receberTemperatura"
                )
                and (
                    temperatura < 12
                    or temperatura > 35
                )
            ):

                enviar_email_alerta(

                    email,

                    cidade,

                    "Temperatura Crítica",

                    (
                        f"Temperatura atual: "
                        f"{temperatura}°C"
                    )
                )

                alerta_disparado = True

            # ======================================
            # SALVA ÚLTIMO ALERTA
            # ======================================

            if alerta_disparado:

                db.collection(
                    "alertas_config"
                ).document(
                    usuario.id
                ).update({

                    "ultimoWeatherCode":
                        codigo
                })

                print(
                    f"[OK] Alerta "
                    f"registrado "
                    f"{cidade}"
                )

        except Exception as e:

            print(
                f"[ERRO] {e}"
            )

# =========================================================
# EXECUÇÃO
# =========================================================

if __name__ == "__main__":

    verificar_alertas()
