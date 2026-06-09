from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.data.pagos import cargar_pagos


def buscar_pago_por_id(id_pago):
    pagos = cargar_pagos()

    for pago in pagos:
        if str(pago.get("id_pago")) == str(id_pago):
            return pago

    return None


def generar_recibo_pdf(id_pago):
    pago = buscar_pago_por_id(id_pago)

    if not pago:
        print("No se encontró el pago.")
        return

    nombre_pdf = f"recibo_pago_{id_pago}.pdf"

    pdf = canvas.Canvas(nombre_pdf, pagesize=letter)

    y = 740

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(190, y, "GM7 IMPRESIÓN")

    y -= 30
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(210, y, "RECIBO DE PAGO")

    y -= 50
    pdf.setFont("Helvetica", 11)

    pdf.drawString(50, y, f"Folio de pago: {pago.get('id_pago')}")
    y -= 20
    pdf.drawString(50, y, f"Cliente: {pago.get('nombre_cliente')}")
    y -= 20
    pdf.drawString(50, y, f"Orden relacionada: {pago.get('id_orden')}")
    y -= 20
    pdf.drawString(50, y, f"Fecha de pago: {pago.get('fecha') or datetime.now().strftime('%d/%m/%Y')}")

    y -= 40
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "DETALLE DEL PAGO")

    y -= 25
    pdf.setFont("Helvetica", 11)

    monto = float(pago.get("monto", 0) or 0)

    pdf.drawString(50, y, f"Monto recibido: ${monto:,.2f}")
    y -= 20
    pdf.drawString(50, y, f"Método de pago: {pago.get('metodo_pago')}")
    y -= 20
    pdf.drawString(50, y, f"Concepto: {pago.get('concepto')}")

    y -= 50

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, "Este documento confirma la recepción del pago registrado en GM7.")

    y -= 60
    pdf.drawString(50, y, "Recibió:")
    pdf.line(120, y, 300, y)

    pdf.save()

    print(f"Recibo PDF generado correctamente: {nombre_pdf}")


if __name__ == "__main__":
    id_pago = input("Ingresa el ID del pago: ")
    generar_recibo_pdf(id_pago)