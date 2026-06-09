import sqlite3


def obtener_conexion():
    conexion = sqlite3.connect("sistema_impresion.db")
    conexion.row_factory = sqlite3.Row

    return conexion
