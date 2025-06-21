import tkinter as tk
from PIL import Image, ImageTk
from conexion import obtener_producto_por_codigo
import os
import sys  # importante para PyInstaller

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, funciona con PyInstaller."""
    try:
        base_path = sys._MEIPASS  # al empaquetar como .exe
    except AttributeError:
        base_path = os.path.abspath(".")  # al correr como .py
    return os.path.join(base_path, relative_path)

def buscar_producto():
    codigo = entry_codigo.get().strip()
    if not codigo:
        return

    nombre, precio = obtener_producto_por_codigo(codigo)

    # Ocultar frame de entrada (fila 0)
    frame_superior.grid_remove()

    if nombre:
        etiqueta_producto.config(text=nombre.upper())
        etiqueta_precio.config(text=f"$ {precio:.2f}")
    else:
        etiqueta_producto.config(text="NO ENCONTRADO")
        etiqueta_precio.config(text="$ 0.00")

    ventana.after(5000, restaurar_interfaz)

def restaurar_interfaz():
    entry_codigo.delete(0, tk.END)
    entry_codigo.focus()

    # Volver a mostrar el frame de entrada (fila 0)
    frame_superior.grid()
    etiqueta_producto.config(text="")
    etiqueta_precio.config(text="")

# Ventana principal
ventana = tk.Tk()
ventana.attributes('-fullscreen', True)
ventana.configure(bg="#D9D9D9")

# Usamos grid para controlar ubicación
ventana.rowconfigure([0, 1, 2], weight=1)
ventana.columnconfigure(0, weight=1)

# Frame para logo + input (fila 0)
frame_superior = tk.Frame(ventana, bg="#D9D9D9")
frame_superior.grid(row=0, column=0)

# Cargar logo
try:
    ruta_logo = resource_path("logo_a.png")
    logo_img = Image.open(ruta_logo)
    logo_img = logo_img.resize((700, 300), Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(frame_superior, image=logo, bg="#D9D9D9")
except Exception as e:
    print(e)
    logo_label = tk.Label(frame_superior, text="LOGO NO ENCONTRADO", font=("Helvetica", 28), fg="black", bg="#D9D9D9")

logo_label.pack()

# Input
entry_codigo = tk.Entry(frame_superior, font=("Helvetica", 36), width=25, justify='center')
entry_codigo.pack(pady=20)
entry_codigo.focus()
entry_codigo.bind('<Return>', lambda e: buscar_producto())

# Resultado precio (fila 2)
etiqueta_precio = tk.Label(ventana, text="", font=("Helvetica", 120, "bold"), fg="black", bg="#D9D9D9")
etiqueta_precio.grid(row=1, column=0)

# Resultado producto (fila 1)
etiqueta_producto = tk.Label(ventana, text="", font=("Helvetica", 30, "bold"), fg="black", bg="#D9D9D9")
etiqueta_producto.grid(row=2, column=0)

# Salida con ESC
ventana.bind('<Escape>', lambda e: ventana.destroy())

ventana.mainloop()
