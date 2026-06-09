from app.data.produccion import listar_produccion_activa_data


def menu_produccion():
    while True:
        print("\n=== MENÚ PRODUCCIÓN ===")
        print("1. Ver producción activa")
        print("2. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            producciones = listar_produccion_activa_data()

            if not producciones:
                print("\nNo hay registros de producción activos.")
            else:
                for p in producciones:
                    print(p)

            input("\nPresiona Enter para volver...")

        elif opcion == "2":
            break

        else:
            print("Opción inválida.")