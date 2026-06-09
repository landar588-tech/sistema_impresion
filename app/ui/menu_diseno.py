from app.modules.diseno import (
    crear_diseno_desde_orden,
    listar_disenos_activos,
    buscar_diseno_por_orden,
    cambiar_estado_diseno,
    cancelar_diseno,
)


def menu_diseno():
    while True:
        print("\n=== MENÚ DE DISEÑO ===")
        print("1. Crear diseño desde orden")
        print("2. Listar diseños activos")
        print("3. Buscar diseño por orden")
        print("4. Cambiar estado de diseño")
        print("5. Cancelar diseño")
        print("6. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            crear_diseno_desde_orden()
        elif opcion == "2":
            listar_disenos_activos()
        elif opcion == "3":
            buscar_diseno_por_orden()
        elif opcion == "4":
            cambiar_estado_diseno()
        elif opcion == "5":
            cancelar_diseno()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")