from app.data.cotizaciones import cargar_cotizaciones


def crear_cotizacion():
    print("\n--- Crear Cotización ---")
    print("Módulo crear cotización pendiente de completar.")


def listar_cotizaciones():
    print("\n--- Lista de Cotizaciones Activas ---")
    cotizaciones = cargar_cotizaciones()
    if not cotizaciones:
        print("No hay cotizaciones registradas.")
        return

    for c in cotizaciones:
        print(c)


def buscar_cotizacion():
    print("\n--- Buscar Cotización ---")
    print("Módulo buscar cotización pendiente de completar.")


def ver_cotizacion():
    print("\n--- Ver Cotización ---")
    print("Módulo ver cotización pendiente de completar.")


def cancelar_cotizacion_ui():
    print("\n--- Cancelar Cotización ---")
    print("Módulo cancelar cotización pendiente de completar.")