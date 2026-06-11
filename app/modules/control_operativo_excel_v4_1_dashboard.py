# -*- coding: utf-8 -*-
"""
control_operativo_excel_v4_1_dashboard.py
===============================================================================
FullColor · CONTROL OPERATIVO — V4.1 (rediseño SOLO del DASHBOARD)
-------------------------------------------------------------------------------
Este script NO modifica ni reemplaza la V4 estable. Reutiliza por import los
constructores estables de `control_operativo_excel_v4.py`:

    - construir_trabajos       -> hoja TRABAJOS  (folios FC, validaciones,
                                  protección y TODAS las fórmulas intactas)
    - construir_pagos          -> hoja PAGOS     (intacta)
    - construir_datos_empresa  -> hoja DATOS_EMPRESA (intacta)

y SOLO redefine la hoja DASHBOARD con un diseño ejecutivo, limpio y colorido.
Las tablas auxiliares que alimentan las gráficas se colocan en una hoja
OCULTA llamada AUX_DASHBOARD (no se muestran en DASHBOARD).

Ejecución (Windows), desde la raíz del proyecto:
    py app\\modules\\control_operativo_excel_v4_1_dashboard.py

Salida:
    FullColor_Control_Operativo_V4_1_Dashboard.xlsx
===============================================================================
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, PieChart, LineChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.marker import Marker
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties

# Reutilizamos la V4 estable SIN modificarla. Al ejecutar este archivo con
# `py app\modules\...py`, la carpeta app/modules queda en sys.path, por lo que
# el import directo del módulo hermano funciona.
import control_operativo_excel_v4 as v4

# Atajos a constantes de negocio de la V4 (rango operativo de TRABAJOS).
FI = v4.FILA_INICIO   # 3
FF = v4.FILA_FIN      # 202
DINERO = '"$"#,##0.00'

# ---------------------------------------------------------------------------
# Paleta del dashboard (clara, diferenciada y profesional)
# ---------------------------------------------------------------------------
AZUL_OSCURO = "1A3A5C"
AZUL = "2E5F8A"
AZUL_EST = "4472C4"
VERDE_HDR = "1E6B3C"
VERDE_OK = "2E9E5B"   # Entregado / Liquidado
ROJO = "C00000"       # Por cobrar / Cancelado
NARANJA = "ED7D31"
NARANJA2 = "C55A11"
AMARILLO = "FFC000"
GRIS = "808080"
MORADO = "7030A0"
MAGENTA = "B4009E"
BLANCO = "FFFFFF"
FONDO_VALOR = "F5F9FF"

# Colores por estado para la gráfica de Status (Entregado en verde).
STATUS = ["Pendiente", "En diseño", "En producción",
          "Listo para entrega", "Entregado", "Cancelado"]
STATUS_COLORS = [GRIS, AZUL_EST, NARANJA, AMARILLO, VERDE_OK, ROJO]


# ===========================================================================
# Utilidades visuales del dashboard
# ===========================================================================
def _solido(color):
    """GraphicalProperties con relleno sólido."""
    return GraphicalProperties(solidFill=color)


def _colorear_puntos(serie, colores):
    """Asigna un color distinto a cada punto/sector de una serie."""
    for idx, color in enumerate(colores):
        dp = DataPoint(idx=idx)
        dp.graphicalProperties = _solido(color)
        serie.data_points.append(dp)


def _banda(ws, fila, texto, color, ncols=14):
    """Encabezado de sección que abarca todo el ancho del tablero."""
    ws.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=ncols)
    c = ws.cell(row=fila, column=1, value=texto)
    c.font = Font(name="Arial", bold=True, size=11, color=BLANCO)
    c.fill = PatternFill("solid", start_color=color)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[fila].height = 20


def _tarjeta(ws, fila, col, titulo, formula, color, span=2, formato=None):
    """
    Tarjeta KPI: rótulo (arriba, con color) + valor grande (abajo).
    Abarca `span` columnas para un aspecto de 'card' amplio.
    """
    ultima = col + span - 1
    ws.merge_cells(start_row=fila, start_column=col, end_row=fila, end_column=ultima)
    ws.merge_cells(start_row=fila + 1, start_column=col, end_row=fila + 1, end_column=ultima)

    t = ws.cell(row=fila, column=col, value=titulo)
    t.font = Font(name="Arial", bold=True, size=9, color=BLANCO)
    t.fill = PatternFill("solid", start_color=color)
    t.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    v = ws.cell(row=fila + 1, column=col, value=formula)
    v.font = Font(name="Arial", bold=True, size=16, color=color)
    v.fill = PatternFill("solid", start_color=FONDO_VALOR)
    v.alignment = Alignment(horizontal="center", vertical="center")
    if formato:
        v.number_format = formato

    # Borde envolvente en toda la tarjeta (ambas filas, todas las columnas).
    for r in (fila, fila + 1):
        for c in range(col, ultima + 1):
            ws.cell(row=r, column=c).border = v4.borde(color, "medium")

    ws.row_dimensions[fila].height = 16
    ws.row_dimensions[fila + 1].height = 30


# ===========================================================================
# Hoja oculta AUX_DASHBOARD (datos que alimentan las gráficas)
# ===========================================================================
def construir_aux_dashboard(wb):
    """
    Crea la hoja AUX_DASHBOARD (oculta) con las tablas auxiliares.
    Distribución en columnas A..E:
        Status        -> A1:B7
        Pago Completo -> A10:B12
        Finanzas      -> A15:B18
        Ventas semana -> A21:E27   (A=Semana B=Ventas C=Inicio D=Fin E=Pico)
        Ventas mes    -> A30:D36   (A=Mes    B=Ventas C=Inicio D=Fin)
    """
    aux = wb.create_sheet("AUX_DASHBOARD")

    def enc(celda, texto):
        c = aux[celda]
        c.value = texto
        c.font = Font(bold=True, color=AZUL_OSCURO, size=9)
        c.fill = PatternFill("solid", start_color="EBF1F8")

    # --- Status (conteos por estado) ---
    enc("A1", "Status")
    enc("B1", "Cantidad")
    for i, estado in enumerate(STATUS, start=2):
        aux.cell(row=i, column=1, value=estado)
        aux.cell(row=i, column=2,
                 value=f'=COUNTIF(TRABAJOS!Q{FI}:Q{FF},"{estado}")')

    # --- Pago Completo (cuenta R="Sí"/"No"; etiquetas Liquidado/Por cobrar) ---
    enc("A10", "Pago")
    enc("B10", "Cantidad")
    aux["A11"] = "Liquidado"
    aux["B11"] = f'=COUNTIF(TRABAJOS!R{FI}:R{FF},"Sí")'
    aux["A12"] = "Por cobrar"
    aux["B12"] = f'=COUNTIF(TRABAJOS!R{FI}:R{FF},"No")'

    # --- Resumen Financiero ---
    enc("A15", "Concepto")
    enc("B15", "Monto")
    aux["A16"] = "Ventas"
    aux["B16"] = f'=SUM(TRABAJOS!I{FI}:I{FF})'
    aux["A17"] = "Anticipos"
    aux["B17"] = f'=SUM(TRABAJOS!K{FI}:K{FF})'
    aux["A18"] = "Saldo pendiente"
    aux["B18"] = f'=SUM(TRABAJOS!L{FI}:L{FF})'
    for r in (16, 17, 18):
        aux.cell(row=r, column=2).number_format = DINERO

    # --- Ventas por semana (últimas 6; semana = lunes a domingo) ---
    enc("A21", "Semana")
    enc("B21", "Ventas")
    enc("C21", "Inicio")
    enc("D21", "Fin")
    enc("E21", "Pico")
    s_ini, s_fin = 22, 27
    for r in range(s_ini, s_fin + 1):
        atras = s_fin - r  # r=27 -> 0 (semana actual)
        aux.cell(row=r, column=3,
                 value=f"=TODAY()-WEEKDAY(TODAY(),2)+1-7*{atras}")
        aux.cell(row=r, column=4, value=f"=C{r}+6")
        aux.cell(row=r, column=1, value=f'=TEXT(C{r},"dd/mm")')
        aux.cell(row=r, column=2,
                 value=(f'=SUMIFS(TRABAJOS!$I${FI}:$I${FF},'
                        f'TRABAJOS!$B${FI}:$B${FF},">="&C{r},'
                        f'TRABAJOS!$B${FI}:$B${FF},"<="&D{r})'))
        # Pico: sólo conserva el máximo (>0); el resto NA() y no se grafica.
        aux.cell(row=r, column=5,
                 value=(f'=IF(AND(B{r}=MAX($B${s_ini}:$B${s_fin}),B{r}>0),'
                        f'B{r},NA())'))
        aux.cell(row=r, column=2).number_format = DINERO
        aux.cell(row=r, column=5).number_format = DINERO

    # --- Ventas por mes (últimos 6) ---
    enc("A30", "Mes")
    enc("B30", "Ventas")
    enc("C30", "Inicio")
    enc("D30", "Fin")
    m_ini, m_fin = 31, 36
    for r in range(m_ini, m_fin + 1):
        atras = m_fin - r  # r=36 -> 0 (mes actual)
        aux.cell(row=r, column=3,
                 value=f"=DATE(YEAR(TODAY()),MONTH(TODAY())-{atras},1)")
        aux.cell(row=r, column=4, value=f"=EOMONTH(C{r},0)")
        aux.cell(row=r, column=1, value=f'=TEXT(C{r},"mmm yy")')
        aux.cell(row=r, column=2,
                 value=(f'=SUMIFS(TRABAJOS!$I${FI}:$I${FF},'
                        f'TRABAJOS!$B${FI}:$B${FF},">="&C{r},'
                        f'TRABAJOS!$B${FI}:$B${FF},"<="&D{r})'))
        aux.cell(row=r, column=2).number_format = DINERO

    # Ocultar y proteger la hoja auxiliar.
    aux.sheet_state = "hidden"
    v4.proteger(aux)
    return aux


# ===========================================================================
# Gráficas (todas leen de AUX_DASHBOARD; se anclan en DASHBOARD sin solaparse)
# ===========================================================================
def _grafica_status(aux, ws, ancla):
    ch = PieChart()
    ch.title = "Trabajos por Status"
    ch.width = 7
    ch.height = 8
    datos = Reference(aux, min_col=2, min_row=1, max_row=7)   # B1 (título) + B2:B7
    cats = Reference(aux, min_col=1, min_row=2, max_row=7)
    ch.add_data(datos, titles_from_data=True)
    ch.set_categories(cats)
    ch.dataLabels = DataLabelList()
    ch.dataLabels.showVal = True
    ch.dataLabels.showPercent = True
    _colorear_puntos(ch.series[0], STATUS_COLORS)  # Entregado en verde
    ws.add_chart(ch, ancla)


def _grafica_pago(aux, ws, ancla):
    ch = PieChart()
    ch.title = "Pago Completo"
    ch.width = 7
    ch.height = 8
    datos = Reference(aux, min_col=2, min_row=10, max_row=12)  # B10 + B11:B12
    cats = Reference(aux, min_col=1, min_row=11, max_row=12)
    ch.add_data(datos, titles_from_data=True)
    ch.set_categories(cats)
    ch.dataLabels = DataLabelList()
    ch.dataLabels.showVal = True
    ch.dataLabels.showPercent = True
    _colorear_puntos(ch.series[0], [VERDE_OK, ROJO])  # Liquidado verde / Por cobrar rojo
    ws.add_chart(ch, ancla)


def _grafica_finanzas(aux, ws, ancla):
    ch = BarChart()
    ch.type = "col"
    ch.title = "Resumen Financiero"
    ch.width = 7
    ch.height = 8
    datos = Reference(aux, min_col=2, min_row=15, max_row=18)  # B15 + B16:B18
    cats = Reference(aux, min_col=1, min_row=16, max_row=18)
    ch.add_data(datos, titles_from_data=True)
    ch.set_categories(cats)
    ch.legend = None
    ch.dataLabels = DataLabelList()
    ch.dataLabels.showVal = True
    ch.dataLabels.numFmt = '"$"#,##0'
    ch.y_axis.numFmt = '"$"#,##0'
    ch.y_axis.title = "Monto"
    _colorear_puntos(ch.series[0], [AZUL, VERDE_OK, NARANJA])  # Ventas/Anticipos/Saldo
    ws.add_chart(ch, ancla)


def _grafica_linea(aux, ws, titulo, ancla, hdr, primero, ultimo,
                   color=AZUL, pico_col=None):
    ch = LineChart()
    ch.title = titulo
    ch.width = 9.5
    ch.height = 8
    datos = Reference(aux, min_col=2, min_row=hdr, max_row=ultimo)
    cats = Reference(aux, min_col=1, min_row=primero, max_row=ultimo)
    ch.add_data(datos, titles_from_data=True)
    ch.set_categories(cats)
    ch.y_axis.numFmt = '"$"#,##0'
    ch.y_axis.title = "Ventas ($)"
    ch.x_axis.delete = False
    ch.y_axis.delete = False

    s = ch.series[0]
    s.smooth = False
    s.marker = Marker(symbol="circle", size=6)
    s.graphicalProperties = GraphicalProperties()
    s.graphicalProperties.line = LineProperties(solidFill=color, w=22000)
    s.dLbls = DataLabelList()
    s.dLbls.showVal = True
    s.dLbls.numFmt = '"$"#,##0'

    # Serie "Pico" (opcional): marca la semana de mayores ventas en rojo.
    if pico_col:
        pico = Reference(aux, min_col=pico_col, min_row=hdr, max_row=ultimo)
        ch.add_data(pico, titles_from_data=True)
        sp = ch.series[1]
        sp.smooth = False
        sp.marker = Marker(symbol="circle", size=12)
        sp.marker.graphicalProperties = _solido("FF0000")
        sp.graphicalProperties = GraphicalProperties()
        sp.graphicalProperties.line = LineProperties(noFill=True)
        sp.dLbls = DataLabelList()
        sp.dLbls.showVal = True

    ws.add_chart(ch, ancla)


# ===========================================================================
# Hoja DASHBOARD (rediseño ejecutivo)
# ===========================================================================
def construir_dashboard_v41(wb):
    """Construye la hoja DASHBOARD nueva + la hoja oculta AUX_DASHBOARD."""
    ws = wb.create_sheet("DASHBOARD")
    aux = construir_aux_dashboard(wb)

    # Lienzo limpio: sin líneas de cuadrícula y columnas uniformes.
    ws.sheet_view.showGridLines = False
    for col in range(1, 15):  # A..N
        ws.column_dimensions[v4.get_column_letter(col)].width = 11

    # --- Título principal ---
    ws.merge_cells("A1:N1")
    ws["A1"] = "FULLCOLOR · DASHBOARD EJECUTIVO"
    ws["A1"].font = Font(name="Arial", bold=True, size=18, color=BLANCO)
    ws["A1"].fill = PatternFill("solid", start_color=AZUL_OSCURO)
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 38

    # Columnas de inicio de cada tarjeta (5 tarjetas, span 2, con hueco).
    cols = [1, 4, 7, 10, 13]  # A, D, G, J, M

    # --- Banda 1: KPIs financieros ---
    _banda(ws, 2, "RESUMEN FINANCIERO", AZUL_OSCURO)
    fin = [
        ("Total Ventas",   f'=SUM(TRABAJOS!I{FI}:I{FF})',            AZUL_OSCURO, DINERO),
        ("Anticipos",      f'=SUM(TRABAJOS!K{FI}:K{FF})',            VERDE_HDR,   DINERO),
        ("Saldo Pendiente", f'=SUM(TRABAJOS!L{FI}:L{FF})',           NARANJA2,    DINERO),
        ("Liquidados",     f'=COUNTIF(TRABAJOS!R{FI}:R{FF},"Sí")',   VERDE_OK,    None),
        ("Por Cobrar",     f'=COUNTIF(TRABAJOS!R{FI}:R{FF},"No")',   ROJO,        None),
    ]
    for c, (titulo, formula, color, fmt) in zip(cols, fin):
        _tarjeta(ws, 3, c, titulo, formula, color, span=2, formato=fmt)

    # --- Banda 2: KPIs de producción ---
    _banda(ws, 6, "ESTADO DE PRODUCCIÓN", AZUL)
    prod = [
        ("Pendientes",    f'=COUNTIF(TRABAJOS!Q{FI}:Q{FF},"Pendiente")',          GRIS),
        ("En Diseño",     f'=COUNTIF(TRABAJOS!Q{FI}:Q{FF},"En diseño")',          AZUL_EST),
        ("En Producción", f'=COUNTIF(TRABAJOS!Q{FI}:Q{FF},"En producción")',      NARANJA),
        ("Listos",        f'=COUNTIF(TRABAJOS!Q{FI}:Q{FF},"Listo para entrega")', AMARILLO),
        ("Entregados",    f'=COUNTIF(TRABAJOS!Q{FI}:Q{FF},"Entregado")',          VERDE_OK),
    ]
    for c, (titulo, formula, color) in zip(cols, prod):
        _tarjeta(ws, 7, c, titulo, formula, color, span=2)

    # --- Banda 3: KPIs de diseño y prioridades ---
    _banda(ws, 10, "DISEÑO Y PRIORIDADES", MORADO)
    dis = [
        ("Trae Diseño",    f'=COUNTIF(TRABAJOS!G{FI}:G{FF},"Sí")',         MORADO),
        ("Requiere Diseño", f'=COUNTIF(TRABAJOS!G{FI}:G{FF},"No")',        MAGENTA),
        ("Prioritarios",   f'=COUNTIF(TRABAJOS!P{FI}:P{FF},"Prioritaria")', NARANJA2),
        ("Alta Prioridad", f'=COUNTIF(TRABAJOS!P{FI}:P{FF},"Alta")',       NARANJA),
        ("Total Trabajos", f'=COUNTIF(TRABAJOS!B{FI}:B{FF},"<>")',         AZUL_OSCURO),
    ]
    for c, (titulo, formula, color) in zip(cols, dis):
        _tarjeta(ws, 11, c, titulo, formula, color, span=2)

    # --- Banda 4: tres gráficas alineadas horizontalmente ---
    _banda(ws, 13, "INDICADORES VISUALES", AZUL_OSCURO)
    _grafica_status(aux, ws, "A15")
    _grafica_pago(aux, ws, "F15")
    _grafica_finanzas(aux, ws, "K15")

    # --- Banda 5: tendencia de ventas (semana y mes) ---
    _banda(ws, 32, "TENDENCIA DE VENTAS", VERDE_HDR)
    _grafica_linea(aux, ws, "Ventas por Semana (últimas 6)", "A34",
                   hdr=21, primero=22, ultimo=27, color=AZUL, pico_col=5)
    _grafica_linea(aux, ws, "Ventas por Mes (últimos 6)", "H34",
                   hdr=30, primero=31, ultimo=36, color=VERDE_HDR)

    # Protegemos la hoja (sólo lectura, como el resto del libro).
    v4.proteger(ws)


# ===========================================================================
# Orquestador
# ===========================================================================
def crear_control_operativo_v41():
    """
    Genera el libro completo reutilizando la V4 estable para TRABAJOS, PAGOS y
    DATOS_EMPRESA, y aplicando el DASHBOARD rediseñado.
    """
    wb = Workbook()

    v4.construir_trabajos(wb)        # TRABAJOS (intacta)
    v4.construir_pagos(wb)           # PAGOS (intacta)
    construir_dashboard_v41(wb)      # DASHBOARD nuevo + AUX_DASHBOARD oculta
    v4.construir_datos_empresa(wb)   # DATOS_EMPRESA (intacta)

    ruta = "FullColor_Control_Operativo_V4_1_Dashboard.xlsx"
    wb.save(ruta)

    print("✅ Archivo guardado:", ruta)
    print("📋 Hojas creadas:", wb.sheetnames)
    print("🙈 Hoja auxiliar oculta:", "AUX_DASHBOARD")


if __name__ == "__main__":
    crear_control_operativo_v41()
