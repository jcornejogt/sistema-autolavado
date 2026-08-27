from datetime import datetime

FECHA_VENCIMIENTO = "2026-09-02"


def licencia_valida():
    fecha_actual = datetime.now().date()
    fecha_vencimiento = datetime.strptime(
        FECHA_VENCIMIENTO,
        "%Y-%m-%d"
    ).date()

    return fecha_actual <= fecha_vencimiento


def dias_restantes():
    fecha_actual = datetime.now().date()
    fecha_vencimiento = datetime.strptime(
        FECHA_VENCIMIENTO,
        "%Y-%m-%d"
    ).date()

    return (fecha_vencimiento - fecha_actual).days
