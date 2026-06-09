from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.data.cotizaciones import cargar_cotizaciones


def buscar_cotizacion_por_id(id_cotizacion):
    cotizaciones = cargar_cotizaciones()

    for cotizacion in cotizaciones:
        if str(cotizacion.get("id_cotizacion")) == str(id_cotizacion):
            return cotizacion

    return None


def generar_cotizacion_pdf(id_cotizacion):
    cotizacion = buscar_cotizacion_por_id(id_cotizacion)

    if not cotizacion:
        print("No se encontró la cotización.")
        return

    nombre_pdf = f"cotizacion_{id_cotizacion}.pdf"

    pdf = canvas.Canvas(nombre_pdf, pagesize=letter)
    ancho, alto = letter

    y = alto - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(180, y, "GM7 IMPRESIÓN")

    y -= 25
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(210, y, "COTIZACIÓN")

    y -= 40
    pdf.setFont("Helvetica", 11)

    pdf.drawString(50, y, f"Folio: {cotizacion.get('id_cotizacion')}")
    y -= 20
    pdf.drawString(50, y, f"Cliente: {cotizacion.get('nombre_cliente')}")
    y -= 20
    pdf.drawString(50, y, f"Fecha: {cotizacion.get('fecha') or datetime.now().strftime('%d/%m/%Y')}")

    y -= 40

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "DETALLE DEL SERVICIO")

    y -= 25
    pdf.setFont("Helvetica", 11)

    pdf.drawString(50, y, f"Producto / Material: {cotizacion.get('producto_material')}")
    y -= 20
    pdf.drawString(50, y, f"Cantidad: {cotizacion.get('cantidad')}")
    y -= 20
    pdf.drawString(50, y, f"Descripción: {cotizacion.get('descripcion')}")

    y -= 40

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "RESUMEN DE COSTOS")

    y -= 25
    pdf.setFont("Helvetica", 11)

    total = float(cotizacion.get("total", 0) or 0)
    anticipo = float(cotizacion.get("anticipo_requerido", 0) or 0)
    saldo = total - anticipo

    pdf.drawString(50, y, f"Total: ${total:,.2f}")
    y -= 20
    pdf.drawString(50, y, f"Anticipo sugerido: ${anticipo:,.2f}")
    y -= 20
    pdf.drawString(50, y, f"Saldo estimado: ${saldo:,.2f}")

    y -= 40

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "Vigencia de cotización: 15 días")

    y -= 40
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, "Gracias por considerar GM7 Impresión.")

    pdf.save()

    print(f"Cotización PDF generada correctamente: {nombre_pdf}")


if __name__ == "__main__":
    id_cotizacion = input("Ingresa el ID de la cotización: ")
    generar_cotizacion_pdf(id_cotizacion)