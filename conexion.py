import pyodbc

def conectar_bd():
    try:
        conexion = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=LAPTOP-LV\\CONTPAC;'
            'DATABASE=adCARDENAS_E_HIJOS_SA;'
            'UID=sa;'
            'PWD=lkqaz923'
        )
        return conexion
    except Exception as e:
        print("Error al conectar a SQL Server:", e)
        return None

def obtener_producto_por_codigo(codigo):
    conexion = conectar_bd()
    if not conexion:
        return None, None

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                aP.CCODIGOPRODUCTO AS codigo,
                aP.CNOMBREPRODUCTO AS nombre,
                admExistenciaCosto.CENTRADASPERIODO12 - admExistenciaCosto.CSALIDASPERIODO12 AS existencia,
                ROUND(aP.CPRECIO1, 2) AS precio,
                ROUND(aP.CPRECIO2, 2) AS mayoreo_Xalapa
            FROM
                [adCARDENAS_E_HIJOS_SA].[dbo].[admExistenciaCosto]
            INNER JOIN admProductos aP ON admExistenciaCosto.CIDPRODUCTO = aP.CIDPRODUCTO
            INNER JOIN admAlmacenes aA ON admExistenciaCosto.CIDALMACEN = aA.CIDALMACEN
            INNER JOIN admEjercicios aE ON admExistenciaCosto.CIDEJERCICIO = aE.CIDEJERCICIO
            WHERE 
                aE.CEJERCICIO = 2024
                AND aP.CSTATUSPRODUCTO = 1 
                AND aA.CNOMBREALMACEN = 'ALMACEN ORIZABA'
                AND (aP.CCODALTERN = ? OR aP.CCODIGOPRODUCTO = ?)
        """, (codigo, codigo))

        resultado = cursor.fetchone()
        if resultado:
            nombre = resultado.nombre
            precio = resultado.precio * 1.16 # o puedes usar mayoreo_Xalapa
            return nombre, precio
        else:
            return None, None
    except Exception as e:
        print("Error en la consulta:", e)
        return None, None
    finally:
        conexion.close()
