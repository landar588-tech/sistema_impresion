from app.data.pagos import listar_pagos_activos


def menu_pagos():
    while True:
        print("\n=== MENÚ PAGOS ===")
        print("1. Ver pagos activos")
        print("2. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            pagos = listar_pagos_activos()

            if not pagos:
                print("\nNo hay pagos activos.")
            else:
                for p in pagos:
                    print(p)

            input("\nPresiona Enter para volver...")

        elif opcion == "2":
            break

        else:
            print("Opción inválida.")