from app.modules.cotizaciones import (
    crear_cotizacion,
    listar_cotizaciones,
    buscar_cotizacion,
    ver_cotizacion,
    cancelar_cotizacion_ui,
)


def menu_cotizaciones():
    while True:
        print("\n=== MENÚ DE COTIZACIONES ===")
        print("1. Crear cotización")
        print("2. Listar cotizaciones activas")
        print("3. Buscar cotización")
        print("4. Ver detalle de cotización")
        print("5. Cancelar cotización")
        print("6. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            crear_cotizacion()
        elif opcion == "2":
            listar_cotizaciones()
        elif opcion == "3":
            buscar_cotizacion()
        elif opcion == "4":
            ver_cotizacion()
        elif opcion == "5":
            cancelar_cotizacion_ui()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")