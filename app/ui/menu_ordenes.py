from app.modules.proyectos import (
    crear_orden_desde_cotizacion,
    listar_ordenes_activas,
    buscar_orden,
    ver_detalle_orden,
    cambiar_estado_orden,
    cancelar_orden,
)


def menu_ordenes():
    while True:
        print("\n=== MENÚ ÓRDENES / PROYECTOS ===")
        print("1. Crear orden desde cotización")
        print("2. Listar órdenes activas")
        print("3. Buscar orden")
        print("4. Ver detalle de orden")
        print("5. Cambiar estado de orden")
        print("6. Cancelar orden")
        print("7. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            crear_orden_desde_cotizacion()
        elif opcion == "2":
            listar_ordenes_activas()
        elif opcion == "3":
            buscar_orden()
        elif opcion == "4":
            ver_detalle_orden()
        elif opcion == "5":
            cambiar_estado_orden()
        elif opcion == "6":
            cancelar_orden()
        elif opcion == "7":
            break
        else:
            print("Opción inválida.")