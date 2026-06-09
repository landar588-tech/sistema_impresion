from datetime import datetime

from app.data.ordenes import cargar_ordenes


def buscar_orden_por_id(id_orden):
    ordenes = cargar_ordenes()

    for orden in ordenes:
        if str(orden.get("id_orden")) == str(id_orden):
            return orden

    return None


def generar_orden_trabajo_txt(id_orden):
    orden = buscar_orden_por_id(id_orden)

    if not orden:
        print("No se encontró la orden.")
        return

    nombre_archivo = f"orden_trabajo_{id_orden}.txt"

    contenido = f"""
========================================
        GM7 IMPRESIÓN
        ORDEN DE TRABAJO
========================================

Folio: {orden.get("id_orden")}
Cliente: {orden.get("nombre_cliente")}
Fecha de impresión: {datetime.now().strftime("%d/%m/%Y %H:%M")}

----------------------------------------
DATOS DEL PEDIDO
----------------------------------------
Producto / Material: {orden.get("producto_material")}
Cantidad: {orden.get("cantidad")}
Descripción: {orden.get("descripcion")}

Fecha estimada de entrega: {orden.get("fecha_estimada_entrega")}
Estado: {orden.get("estado")}

----------------------------------------
DATOS DE PAGO
----------------------------------------
Anticipo requerido: ${float(orden.get("anticipo_requerido", 0) or 0):,.2f}
Anticipo pagado: ${float(orden.get("anticipo_pagado", 0) or 0):,.2f}
Saldo pendiente: ${float(orden.get("saldo_pendiente", 0) or 0):,.2f}

----------------------------------------
OBSERVACIONES DE PRODUCCIÓN
----------------------------------------
____________________________________________________

____________________________________________________

____________________________________________________

----------------------------------------
FIRMA / AUTORIZACIÓN
----------------------------------------
Recibió: _______________________________

Autorizó: ______________________________
"""

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)

    print(f"Orden de trabajo generada correctamente: {nombre_archivo}")


if __name__ == "__main__":
    id_orden = input("Ingresa el ID de la orden: ")
    generar_orden_trabajo_txt(id_orden)