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
