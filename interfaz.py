import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from conexion import obtener_producto_por_codigo

def buscar_producto():
    codigo = entry_codigo.get()
    nombre, precio = obtener_producto_por_codigo(codigo)
    
    if nombre:
        etiqueta_producto.config(text=nombre.upper())
        etiqueta_precio.config(text=f"$ {precio:.2f}")
    else:
        etiqueta_producto.config(text="NO ENCONTRADO")
        etiqueta_precio.config(text="$ 0.00")

    # Esperar 5 segundos y limpiar entrada
    ventana.after(5000, limpiar)

def limpiar():
    entry_codigo.delete(0, tk.END)
    etiqueta_producto.config(text="")
    etiqueta_precio.config(text="")
    entry_codigo.focus()

# Ventana principal
ventana = tk.Tk()
ventana.attributes('-fullscreen', True)
ventana.configure(bg="#D9D9D9")  # fondo gris claro

# Cargar y mostrar logo
try:
    logo_img = Image.open("logo_a.png")
    logo_img = logo_img.resize((700, 300), Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(logo_img)
    tk.Label(ventana, image=logo, bg="#D9D9D9").pack(pady=10)
except Exception as e:
    print(e)
    tk.Label(ventana, text="LOGO NO ENCONTRADO", font=("Helvetica", 28), fg="black", bg="#D9D9D9").pack(pady=10)

# # Instrucción
# tk.Label(
#     ventana,
#     text="Coloca el código bajo el escáner para obtener el precio",
#     font=("Helvetica", 24),
#     fg="black",
#     bg="#D9D9D9"
# ).pack()

# Entrada de código
entry_codigo = tk.Entry(ventana, font=("Helvetica", 36), width=25, justify='center')
entry_codigo.pack(pady=30)
entry_codigo.focus()
entry_codigo.bind('<Return>', lambda e: buscar_producto())

# Resultado nombre
etiqueta_producto = tk.Label(ventana, text="", font=("Helvetica", 40, "bold"), fg="black", bg="#D9D9D9")
etiqueta_producto.pack(pady=20)

# Resultado precio
etiqueta_precio = tk.Label(ventana, text="", font=("Helvetica", 60, "bold"), fg="black", bg="#D9D9D9")
etiqueta_precio.pack()

# Salida con ESC
ventana.bind('<Escape>', lambda e: ventana.destroy())

ventana.mainloop()
