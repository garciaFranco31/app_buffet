import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import sqlite3
import csv
import os
from datetime import datetime

# Conexión a la base de datos SQLite
def conectar_db():
    return sqlite3.connect('buffet_stock.db')

# Inicializar la base de datos y tabla de stock
def inicializar_db():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Función para cargar una nueva venta
def cargar_venta():
    # Obtener productos del stock
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, cantidad, precio FROM stock')
    productos = cursor.fetchall()
    conn.close()
    
    if not productos:
        messagebox.showerror("Error", "No hay productos en stock.")
        return
    
    # Ventana para seleccionar productos
    venta_window = tk.Toplevel(root)
    venta_window.title("Cargar Nueva Venta")
    
    tk.Label(venta_window, text="Selecciona productos y cantidades:").pack()
    
    productos_seleccionados = {}
    
    for prod in productos:
        frame = tk.Frame(venta_window)
        frame.pack()
        tk.Label(frame, text=f"{prod[1]} (Stock: {prod[2]}, Precio: ${prod[3]})").pack(side=tk.LEFT)
        qty_var = tk.IntVar()
        tk.Entry(frame, textvariable=qty_var, width=5).pack(side=tk.LEFT)
        productos_seleccionados[prod[0]] = (prod[1], prod[2], prod[3], qty_var)
    
    def confirmar_venta():
        total = 0
        venta_detalles = []
        conn = conectar_db()
        cursor = conn.cursor()
        
        for prod_id, (nombre, stock, precio, qty_var) in productos_seleccionados.items():
            qty = qty_var.get()
            if qty > 0:
                if qty > stock:
                    messagebox.showerror("Error", f"No hay suficiente stock para {nombre}.")
                    conn.close()
                    return
                total += qty * precio
                venta_detalles.append(f"{nombre} x{qty}")
                # Reducir stock
                cursor.execute('UPDATE stock SET cantidad = cantidad - ? WHERE id = ?', (qty, prod_id))
        
        if not venta_detalles:
            messagebox.showerror("Error", "No se seleccionó ningún producto.")
            conn.close()
            return
        
        conn.commit()
        conn.close()
        
        # Registrar en CSV
        fecha = datetime.now().strftime('%Y%m%d')
        hora = datetime.now().strftime('%H:%M:%S')
        archivo_csv = f'ventas-{fecha}.csv'
        with open(archivo_csv, 'a', newline='') as file:
            writer = csv.writer(file)
            if os.stat(archivo_csv).st_size == 0:  # Si es nuevo, agregar encabezado
                writer.writerow(['Fecha', 'Hora', 'Productos', 'Total'])
            writer.writerow([fecha, hora, '; '.join(venta_detalles), f'${total:.2f}'])
        
        messagebox.showinfo("Éxito", f"Venta registrada. Total: ${total:.2f}")
        venta_window.destroy()
    
    tk.Button(venta_window, text="Confirmar Venta", command=confirmar_venta).pack()

# Función para controlar/modificar stock
def controlar_stock():
    stock_window = tk.Toplevel(root)
    stock_window.title("Controlar/Modificar Stock")
    
    # Mostrar stock actual
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, cantidad, precio FROM stock')
    productos = cursor.fetchall()
    conn.close()
    
    tk.Label(stock_window, text="Stock Actual:").pack()
    for prod in productos:
        tk.Label(stock_window, text=f"ID: {prod[0]}, {prod[1]} - Cant: {prod[2]}, Precio: ${prod[3]}").pack()
    
    # Opciones para agregar/modificar
    tk.Label(stock_window, text="Agregar Nuevo Producto:").pack()
    nombre_var = tk.StringVar()
    tk.Entry(stock_window, textvariable=nombre_var, placeholder="Nombre").pack()
    cantidad_var = tk.IntVar()
    tk.Entry(stock_window, textvariable=cantidad_var, placeholder="Cantidad").pack()
    precio_var = tk.DoubleVar()
    tk.Entry(stock_window, textvariable=precio_var, placeholder="Precio").pack()
    
    def agregar_producto():
        nombre = nombre_var.get()
        cantidad = cantidad_var.get()
        precio = precio_var.get()
        if nombre and cantidad > 0 and precio > 0:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO stock (nombre, cantidad, precio) VALUES (?, ?, ?)', (nombre, cantidad, precio))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Producto agregado.")
            stock_window.destroy()
            controlar_stock()  # Recargar
        else:
            messagebox.showerror("Error", "Datos inválidos.")
    
    tk.Button(stock_window, text="Agregar", command=agregar_producto).pack()
    
    # Modificar existente
    tk.Label(stock_window, text="Modificar Producto (por ID):").pack()
    id_var = tk.IntVar()
    tk.Entry(stock_window, textvariable=id_var, placeholder="ID").pack()
    nueva_cantidad_var = tk.IntVar()
    tk.Entry(stock_window, textvariable=nueva_cantidad_var, placeholder="Nueva Cantidad").pack()
    
    def modificar_stock():
        prod_id = id_var.get()
        nueva_cantidad = nueva_cantidad_var.get()
        if prod_id > 0 and nueva_cantidad >= 0:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute('UPDATE stock SET cantidad = ? WHERE id = ?', (nueva_cantidad, prod_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Stock modificado.")
            stock_window.destroy()
            controlar_stock()  # Recargar
        else:
            messagebox.showerror("Error", "Datos inválidos.")
    
    tk.Button(stock_window, text="Modificar", command=modificar_stock).pack()

# Función para descargar reporte de ventas del día
def descargar_reporte():
    fecha = datetime.now().strftime('%Y%m%d')
    archivo_csv = f'ventas-{fecha}.csv'
    if os.path.exists(archivo_csv):
        destino = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialfile=archivo_csv)
        if destino:
            os.rename(archivo_csv, destino)
            messagebox.showinfo("Éxito", f"Reporte descargado como {destino}")
    else:
        messagebox.showerror("Error", "No hay ventas registradas hoy.")

# Inicializar la app
inicializar_db()

# Ventana principal
root = tk.Tk()
root.title("Sistema de Buffet - Ventas y Stock")

tk.Button(root, text="Cargar Nueva Venta", command=cargar_venta).pack(pady=10)
tk.Button(root, text="Controlar/Modificar Stock", command=controlar_stock).pack(pady=10)
tk.Button(root, text="Descargar Reporte de Ventas del Día", command=descargar_reporte).pack(pady=10)

root.mainloop()
