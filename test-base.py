import pyodbc

conn_str = (
    r"DRIVER={SQL Server};"
    r"SERVER=LAPTOP-LV\CONTPAC;"
    r"DATABASE=adCARDENAS_E_HIJOS_SA;"
    r"UID=sa;"
    r"PWD=lkqaz923"
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("SELECT TOP (1) [CNOMBREPRODUCTO] FROM [adCARDENAS_E_HIJOS_SA].[dbo].[admProductos]")
    tablas = cursor.fetchall()

    print("Tablas en la base de datos:")
    for tabla in tablas:
        print(tabla[0])

    cursor.close()
    conn.close()

except Exception as e:
    print("Error:", e)
