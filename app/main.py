from app.ui.menu_dashboard import menu_dashboard
from app.ui.menu_clientes import menu_clientes
from app.ui.menu_cotizaciones import menu_cotizaciones
from app.ui.menu_ordenes import menu_ordenes
from app.ui.menu_diseno import menu_diseno
from app.ui.menu_produccion import menu_produccion
from app.ui.menu_pagos import menu_pagos


def main():
    while True:
        print("\n=== SISTEMA DE DISEÑO E IMPRESIÓN ===")
        print("1. Dashboard")
        print("2. Clientes")
        print("3. Cotizaciones")
        print("4. Órdenes / Proyectos")
        print("5. Diseño")
        print("6. Producción")
        print("7. Pagos")
        print("8. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            menu_dashboard()
        elif opcion == "2":
            menu_clientes()
        elif opcion == "3":
            menu_cotizaciones()
        elif opcion == "4":
            menu_ordenes()
        elif opcion == "5":
            menu_diseno()
        elif opcion == "6":
            menu_produccion()
        elif opcion == "7":
            menu_pagos()
        elif opcion == "8":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
    