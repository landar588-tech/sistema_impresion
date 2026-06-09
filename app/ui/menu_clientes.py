from app.modules.clientes import (
    crear_cliente,
    listar_clientes,
    buscar_cliente,
    editar_cliente,
    eliminar_cliente_logico,
)


def menu_clientes():
    while True:
        print("\n=== MENÚ DE CLIENTES ===")
        print("1. Registrar cliente")
        print("2. Listar clientes activos")
        print("3. Buscar cliente")
        print("4. Editar cliente")
        print("5. Desactivar cliente")
        print("6. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            crear_cliente()
        elif opcion == "2":
            listar_clientes()
        elif opcion == "3":
            buscar_cliente()
        elif opcion == "4":
            editar_cliente()
        elif opcion == "5":
            eliminar_cliente_logico()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")