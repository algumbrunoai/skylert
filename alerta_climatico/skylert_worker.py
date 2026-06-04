from firebase_config import db

from datetime import datetime

from skylert_meteo_service import (
    obter_clima,
    gerar_id_cidade
)

# =========================================================
# ATUALIZA CACHE CLIMÁTICO
# =========================================================

def atualizar_cache_climatico():

    print("\n==============================")
    print("ATUALIZANDO CACHE CLIMÁTICO")
    print("==============================\n")

    docs = db.collection(
        "alertas_config"
    ).stream()

    cidades_unicas = set()

    # ==========================================
    # REMOVE CIDADES DUPLICADAS
    # ==========================================

    for doc in docs:

        dados = doc.to_dict()

        cidade = dados.get(
            "cidadeMonitorada"
        )

        if cidade:
            cidades_unicas.add(cidade)

    print(
        f"{len(cidades_unicas)} "
        f"cidades encontradas.\n"
    )

    # ==========================================
    # CONSULTA CLIMA
    # ==========================================

    for cidade in cidades_unicas:

        try:

            print(
                f"[INFO] Consultando "
                f"{cidade}"
            )

            # Limpa o nome removendo o hífen e o estado (ex: "Boa Vista - Roraima" -> "Boa Vista")
            # Isso garante que a API de Geolocalização encontre a cidade com sucesso!
            cidade_busca = cidade.split(" - ")[0].strip() if " - " in cidade else cidade

            clima = obter_clima(cidade_busca)

            if not clima:

                print(
                    f"[ERRO] Não foi "
                    f"possível obter "
                    f"clima de {cidade}"
                )

                continue

            cidade_id = gerar_id_cidade(
                cidade
            )
            
            db.collection(
                "clima_cache"
            ).document(cidade_id).set({

                "cidade":
                    cidade,

                "weatherCode":
                    clima["weather_code"],

                "descricao":
                    clima["descricao"],

                "temperatura":
                    clima["temperatura"],

                "sensacao":
                    clima["sensacao"],

                "umidade":
                    clima["umidade"],

                "vento":
                    clima["vento"],

                "precipitacao":
                    clima["precipitacao"],

                "chuva":
                    clima["chuva"],

                "isDay":
                    clima["is_day"],

                "ultimaAtualizacao":
                    datetime.utcnow()
            })

            print(
                f"[OK] Cache atualizado {cidade}"
            )

        except Exception as e:

            print(
                f"[ERRO] {cidade}: {e}"
            )

# =========================================================
# EXECUÇÃO
# =========================================================

if __name__ == "__main__":

    atualizar_cache_climatico()
