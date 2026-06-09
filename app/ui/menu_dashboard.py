from app.modules.dashboard import (
    ver_dashboard_general,
    ver_entregas_proximas,
    ver_pagos_pendientes,
)


def menu_dashboard():
    while True:
        print("\n=== MENÚ DASHBOARD ===")
        print("1. Ver dashboard general")
        print("2. Ver entregas próximas")
        print("3. Ver pagos pendientes")
        print("4. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            ver_dashboard_general()
        elif opcion == "2":
            ver_entregas_proximas()
        elif opcion == "3":
            ver_pagos_pendientes()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")