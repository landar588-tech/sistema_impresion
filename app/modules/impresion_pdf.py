from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.data.ordenes import cargar_ordenes


def buscar_orden_por_id(id_orden):
    ordenes = cargar_ordenes()

    for orden in ordenes:
        if str(orden.get("id_orden")) == str(id_orden):
            return orden

    return None


def generar_orden_trabajo_pdf(id_orden):
    orden = buscar_orden_por_id(id_orden)

    if not orden:
        print("No se encontró la orden.")
        return

    nombre_pdf = f"orden_trabajo_{id_orden}.pdf"

    pdf = canvas.Canvas(nombre_pdf, pagesize=letter)
    ancho, alto = letter

    y = alto - 50

    # Encabezado
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(180, y, "GM7 IMPRESIÓN")

    y -= 25
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(190, y, "ORDEN DE TRABAJO")

    y -= 40
    pdf.setFont("Helvetica", 11)

    pdf.drawString(50, y, f"Folio: {orden.get('id_orden')}")
    y -= 20

    pdf.drawString(50, y, f"Cliente: {orden.get('nombre_cliente')}")
    y -= 20

    pdf.drawString(
        50,
        y,
        f"Fecha de impresión: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

    y -= 40

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "DATOS DEL PEDIDO")

    y -= 25
    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        50,
        y,
        f"Producto / Material: {orden.get('producto_material')}"
    )

    y -= 20
    pdf.drawString(50, y, f"Cantidad: {orden.get('cantidad')}")

    y -= 20
    pdf.drawString(
        50,
        y,
        f"Descripción: {orden.get('descripcion')}"
    )

    y -= 20
    pdf.drawString(
        50,
        y,
        f"Fecha estimada de entrega: {orden.get('fecha_estimada_entrega')}"
    )

    y -= 20
    pdf.drawString(50, y, f"Estado: {orden.get('estado')}")

    y -= 40

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "DATOS DE PAGO")

    y -= 25
    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        50,
        y,
        f"Anticipo requerido: ${float(orden.get('anticipo_requerido', 0) or 0):,.2f}"
    )

    y -= 20
    pdf.drawString(
        50,
        y,
        f"Anticipo pagado: ${float(orden.get('anticipo_pagado', 0) or 0):,.2f}"
    )

    y -= 20
    pdf.drawString(
        50,
        y,
        f"Saldo pendiente: ${float(orden.get('saldo_pendiente', 0) or 0):,.2f}"
    )

    y -= 50

    pdf.drawString(50, y, "Firma Producción:")
    pdf.line(170, y, 320, y)

    y -= 40

    pdf.drawString(50, y, "Firma Cliente:")
    pdf.line(150, y, 300, y)

    pdf.save()

    print(f"PDF generado correctamente: {nombre_pdf}")


if __name__ == "__main__":
    id_orden = input("Ingresa el ID de la orden: ")
    generar_orden_trabajo_pdf(id_orden)