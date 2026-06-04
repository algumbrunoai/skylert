import os
import sys

# Adiciona a pasta raiz e a pasta 'servicos' ao caminho de busca do Python
PASTA_RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PASTA_RAIZ)
sys.path.append(os.path.join(PASTA_RAIZ, "servicos"))

import time

from skylert_worker import (
    atualizar_cache_climatico
)

from notification_worker import (
    verificar_alertas
)

while True:

    print("\nINICIANDO CICLO...\n")

    atualizar_cache_climatico()

    verificar_alertas()

    print("\nAGUARDANDO 5 MIN...\n")

    time.sleep(300)
