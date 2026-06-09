from app.database.conexion import obtener_conexion


def _fila_a_diccionario(fila):
    return {
        "id_diseno": fila[0],
        "id_orden": fila[1],
        "fecha_creacion": fila[2],
        "nombre_cliente": fila[3],
        "producto_material": fila[4],
        "descripcion": fila[5],
        "estado_diseno": fila[6],
        "fecha_envio_cliente": fila[7],
        "fecha_aprobacion": fila[8],
        "numero_correcciones": fila[9],
        "observaciones": fila[10],
        "activo": bool(fila[11]),
    }


def cargar_disenos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_diseno, id_orden, fecha_creacion, nombre_cliente,
               producto_material, descripcion, estado_diseno,
               fecha_envio_cliente, fecha_aprobacion, numero_correcciones,
               observaciones, activo
        FROM disenos
    """)

    disenos = [_fila_a_diccionario(fila) for fila in cursor.fetchall()]
    conexion.close()

    return disenos


def generar_id_diseno():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT MAX(id_diseno) FROM disenos")
    ultimo_id = cursor.fetchone()[0]

    conexion.close()

    return 1 if ultimo_id is None else ultimo_id + 1


def agregar_diseno(diseno):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO disenos (
            id_diseno, id_orden, fecha_creacion, nombre_cliente,
            producto_material, descripcion, estado_diseno,
            fecha_envio_cliente, fecha_aprobacion, numero_correcciones,
            observaciones, activo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        diseno.get("id_diseno"),
        diseno.get("id_orden"),
        diseno.get("fecha_creacion"),
        diseno.get("nombre_cliente"),
        diseno.get("producto_material"),
        diseno.get("descripcion"),
        diseno.get("estado_diseno", "Pendiente"),
        diseno.get("fecha_envio_cliente"),
        diseno.get("fecha_aprobacion"),
        diseno.get("numero_correcciones", 0),
        diseno.get("observaciones", ""),
        1 if diseno.get("activo", True) else 0,
    ))

    conexion.commit()
    conexion.close()


def obtener_diseno_por_orden(id_orden):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_diseno, id_orden, fecha_creacion, nombre_cliente,
               producto_material, descripcion, estado_diseno,
               fecha_envio_cliente, fecha_aprobacion, numero_correcciones,
               observaciones, activo
        FROM disenos
        WHERE id_orden = ?
        AND activo = 1
    """, (id_orden,))

    fila = cursor.fetchone()
    conexion.close()

    return _fila_a_diccionario(fila) if fila else None


def obtener_diseno_por_id(id_diseno):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_diseno, id_orden, fecha_creacion, nombre_cliente,
               producto_material, descripcion, estado_diseno,
               fecha_envio_cliente, fecha_aprobacion, numero_correcciones,
               observaciones, activo
        FROM disenos
        WHERE id_diseno = ?
    """, (id_diseno,))

    fila = cursor.fetchone()
    conexion.close()

    return _fila_a_diccionario(fila) if fila else None


def actualizar_diseno(id_diseno, datos_actualizados):
    if not datos_actualizados:
        return False

    campos = []
    valores = []

    for campo, valor in datos_actualizados.items():
        campos.append(f"{campo} = ?")
        valores.append(valor)

    valores.append(id_diseno)

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(f"""
        UPDATE disenos
        SET {", ".join(campos)}
        WHERE id_diseno = ?
    """, valores)

    conexion.commit()
    actualizado = cursor.rowcount > 0
    conexion.close()

    return actualizado


def listar_disenos_activos_data():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_diseno, id_orden, fecha_creacion, nombre_cliente,
               producto_material, descripcion, estado_diseno,
               fecha_envio_cliente, fecha_aprobacion, numero_correcciones,
               observaciones, activo
        FROM disenos
        WHERE activo = 1
    """)

    disenos = [_fila_a_diccionario(fila) for fila in cursor.fetchall()]
    conexion.close()

    return disenos


def cancelar_diseno_data(id_diseno):
    return actualizar_diseno(
        id_diseno,
        {
            "estado_diseno": "Cancelado",
            "activo": 0
        }
    )