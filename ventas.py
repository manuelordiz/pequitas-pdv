import sqlite3
from tkinter import *
import tkinter as tk
from   tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import datetime
import sys
import os


class Ventas(tk.Frame):
    db_name = "database.db"

    def __init__(self, padre):
        super().__init__(padre)
        self.numero_factura_actual = self.obtener_numero_factura_actual()
        self.widgets()
        self.mostrar_numero_factura()
                
    def widgets(self):
        
        frame1 = tk.Frame(self, bg="#8258FA", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1110, height=100)
        
        
        titulo = tk.Label(self, text="Ventas", bg="#8258FA", font="Helvetica 24 bold", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)
        
        frame2 = tk.Frame(self, bg="#8181F7", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)
        
        lblframe = LabelFrame(frame2, text="Informacion de la venta", bg="#8181F7", font="Helvetica 16")
        lblframe.place(x=10, y=10, width=1050, height=120)
        
        lbl_num_factura = tk.Label(lblframe, text="Numero de \nFactura", bg="#8181F7", font="Helvetica 11")
        lbl_num_factura.place(x=10, y=3)
        self.num_factura = tk.StringVar()
        
        self.entry_num_factura = ttk.Entry(lblframe, textvariable=self.num_factura, state="reandoly", font="Helvetica 10")
        self.entry_num_factura.place(x=110, y=10, width=100)
        
        lbl_nombre = tk.Label(lblframe, text="Productos: ", bg="#8181F7", font="Helvetica 12")
        lbl_nombre.place(x=210, y=12)
        self.entry_nombre = ttk.Combobox(lblframe, font="Helvetica 10", state="readonly")
        self.entry_nombre.place(x=300, y=10, width=180)

        self.cargar_productos()
        
        label_valor = tk.Label(lblframe, text="Precio:", bg="#8181F7", font="Helvetica 12")
        label_valor.place(x=480, y=12)
        self.entry_valor = ttk.Entry(lblframe, font="Helvetica 10", state="readonly")
        self.entry_valor.place(x=540, y=10, width=180)

        self.entry_nombre.bind("<<ComboboxSelected>>", self.actualizar_precio)
        
        label_cantidad = tk.Label(lblframe, text="Cantidad:", bg="#8181F7", font="Helvetica 12")
        label_cantidad.place(x=725, y=12)
        self.entry_cantidad = ttk.Entry(lblframe, font="Helvetica 10")
        self.entry_cantidad.place(x=810, y=10, width=180)
        
        treeframe = tk.Frame(frame2, bg="gray")
        treeframe.place(x=150, y=150, width=800, height=200)
        
        scroll_y = ttk.Scrollbar(treeframe, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = ttk.Scrollbar(treeframe, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        self.tree = ttk.Treeview(treeframe, columns=("Productos", "Precio", "Cantidad", "Subtotal"), show="headings", height=10, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        self.tree.heading("#1", text="Productos")
        self.tree.heading("#2", text="Precio")
        self.tree.heading("#3", text="Cantidad")
        self.tree.heading("#4", text="Subtotal")
        
        self.tree.column("Productos", anchor="center")
        self.tree.column("Precio", anchor="center")
        self.tree.column("Cantidad", anchor="center")
        self.tree.column("Subtotal", anchor="center")

        self.tree.pack(expand=True, fill=BOTH)    
        
        lblframe2 = tk.LabelFrame(frame2, text="Opciones", bg="#8181F7", font="Helvetica 12")
        lblframe2.place(x=10, y=400, width=1060, height=100)
        
        btn_agregar = tk.Button(lblframe2, text="Agregar Articulo", bg="#BDBDBD", font="Helvetica 10", command=self.registrar)
        btn_agregar.place(x=50, y=10, width=240, height=50)
        
        btn_pagar = tk.Button(lblframe2, text="Pagar", bg="#BDBDBD", font="Helvetica 10", command=self.abrir_ventana_pago)
        btn_pagar.place(x=400, y=10, width=240, height=50)
        
        btn_factura = tk.Button(lblframe2, text="Ver Factura", bg="#BDBDBD", font="Helvetica 10", command=self.abrir_ventana_factura)
        btn_factura.place(x=750, y=10, width=240, height=50)

        self.label_suma_total = tk.Label(frame2, text="Total a pagar: $0", bg="#8181F7", font="Helvetica 24")
        self.label_suma_total.place(x=375, y=360, height=50)

    def cargar_productos(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT nombre FROM inventario")
            productos = c.fetchall()
            self.entry_nombre["values"] = [producto[0] for producto in productos]
            if not productos:
                print("No se encontraron porductos en la base de datos")
            conn.close()
        except sqlite3.Error as e:
            print("Error al cargar productos en la base de datos:", e)


    def actualizar_precio(self, event):
        nombre_producto = self.entry_nombre.get()
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT precio FROM inventario WHERE nombre = ?", [nombre_producto])
            precio = c.fetchone()
            if precio:
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, precio[0])
                self.entry_valor.config(state="readonly")
            else:   
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, "Precio no disponible")
                self.entry_valor.config(state="readonly")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener el precio: ¨{e}")
        finally:
            conn.close()

    def actualizar_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values") [3])
            total += subtotal
        self.label_suma_total.config(text=f"Total a pagar: ${total}")

    def registrar(self):
        producto = self.entry_nombre.get()
        precio = self.entry_valor.get()
        cantidad = self.entry_cantidad.get()

        if producto and precio and cantidad:
            try:
                cantidad = int(cantidad)
                if not self.verificar_stock(producto, cantidad):
                    messagebox.showerror("Error", "Stock insuficiente para el producto selecciondo")
                precio = float(precio)
                subtotal = cantidad * precio 

                self.tree.insert("", "end", values=(producto, f"{precio: }", cantidad, f"{subtotal}"))   

                self.entry_nombre.set("")
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.config(state="readonly")
                self.entry_cantidad.delete(0, tk.END)

                self.actualizar_total()
            except ValueError:
                messagebox.showerror("Error", "Cantidad o precio no validos")
        else:
            messagebox.showerror("Error", "Debe completar todos los campos")

    def verificar_stock(self, nombre_producto, cantidad):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT stock FROM Inventario WHERE nombre = ?", (nombre_producto,))
            stock = c.fetchone()
            if stock and stock[0] >= cantidad:
                return True
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al verificar el stock: {e}")
            return False
        finally:
            conn.close()

    def obtener_total(self):
            total = 0.0
            for child in self.tree.get_children():
                subtotal = float(self.tree.item(child, "values") [3])
                total += subtotal
            return total
        
    def abrir_ventana_pago(self):
            if not self.tree.get_children():
                messagebox.showerror("Error", "No hay articulos para pagar")
                return
                
            ventana_pago = Toplevel(self)
            ventana_pago.title("Realizar pago")
            ventana_pago.geometry("400x400")
            ventana_pago.config(bg="#8258FA")
            ventana_pago.resizable(False, False)
                
            label_total = tk.Label(ventana_pago, bg="#8258FA", text=f"Total a pagar: ${self.obtener_total()}", font="Helvetica 18")
            label_total.place(x=75, y=25)

            label_cantidad_pagada = tk.Label(ventana_pago, bg="#8258FA", text="Cantidad pagada", font="Helvetica 14") 
            label_cantidad_pagada.place(x=130, y=90)
            entry_cantidad_pagada = ttk.Entry(ventana_pago, font="Helvetica 10")
            entry_cantidad_pagada.place(x=130, y=140) 

            label_cambio = tk.Label(ventana_pago, bg="#8258FA", text="", font="Helvetica 14") 
            label_cambio.place(x=150, y=200)

            def calcular_cambio():
                try:
                    cantidad_pagada = float(entry_cantidad_pagada.get())  
                    total = self.obtener_total()
                    cambio = cantidad_pagada - total
                    if cambio < 0:
                        messagebox.showerror("Error", "La cantidad pagada es insuficiente")
                        return
                    label_cambio.config(text=f"Vuelto: ${cambio}")
                except ValueError:
                    messagebox.showerror("Error", "Cantidad pagada no valida") 

            boton_calcular = tk.Button(ventana_pago, text="Calcular Vuelto", bg="#BDBDBD", font="Helvetica 12", command=calcular_cambio)
            boton_calcular.place(x=90, y=250, width=240, height=40)

            boton_pagar = tk.Button(ventana_pago, text="Pagar", bg="#BDBDBD", font="Helvetica 12", command=lambda: self.pagar(ventana_pago, entry_cantidad_pagada, label_cambio))
            boton_pagar.place(x=90, y=300, width=240, height=40)

                
    def pagar(self, ventana_pago, entry_cantidad_pagada, label_cambio):
        try:
            cantidad_pagada = float(entry_cantidad_pagada.get())
            total = self.obtener_total()
            cambio = cantidad_pagada - total
            if cambio < 0:
                messagebox.showerror("Error", "La cantidad pagada es insuficiente")
                return
            label_cambio.config(text=f"Vuelto: {cambio}")
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            try:
                productos = []
                for child in self.tree.get_children():
                    item = self.tree.item(child, "values")
                    producto = item[0]
                    precio = item[1]
                    cantidad_vendida = int(item[2])
                    subtotal = float(item[3])
                    productos.append([producto, precio, cantidad_vendida, subtotal])
                    

                c.execute("INSERT INTO Ventas (factura, nombre_articulo, valor_articulo, cantidad, subtotal) VALUES (?,?,?,?,?)", 
                          (self.numero_factura_actual, producto, float(precio), cantidad_vendida, subtotal))
                    
                c.execute("UPDATE inventario SET stock = stock - ? WHERE nombre = ?",(cantidad_vendida, producto))
                          
                conn.commit()
                messagebox.showinfo("Exito", "Venta registrada Exitosamente")

                self.numero_factura_actual += 1
                self.mostrar_numero_factura()

                for child in self.tree.get_children():
                    self.tree.delete(child)
                    self.label_suma_total.config(text="Total a pagar: $0")  

                    ventana_pago.destroy()     
                    
                    fecha = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    self.generar_factura(productos, total, self.numero_factura_actual - 1, fecha)
                    
                    
            except sqlite3.Error as e:
                conn.rollback()
                messagebox.showerror("Erorr", f"Error al registrar la venta: {e}")
                
            finally:
                conn.close()
        except ValueError:
            messagebox.showerror("Error", "Cantidad pagada no valida")      

    def generar_factura(self, productos, total, factura_numero, fecha):
        archivo_pdf = f"facturas/factura_{factura_numero}.pdf"

        c = canvas.Canvas(archivo_pdf, pagesize=letter)
        width, height = letter

        styles = getSampleStyleSheet()
        estilo_titulo = styles["Title"]
        estilo_normal = styles["Normal"]
        
        c.setFont("Helvetica", 16)
        c.drawString(100, height - 50, f"Factura #{factura_numero}")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 70, f"Fecha: {fecha}")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 100, "Informacion de la venta")
        
        data = [["Producto", "Precio", "Cantidad", "Subtotal"]] + productos
        table = Table(data)
        table.wrapOn(c, width, height)
        table.drawOn(c, 100, height - 200)
        
        c.setFont("Helvetica", 16)
        c.drawString(100, height - 250, f"Total a pagar: $ {total}")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 300, "Gracias por su compra, vuelva pontro.")
        
        c.save()
        
        messagebox.showinfo("Factura generada", f"La factura #{factura_numero} ha sido creada con exito")
        
        os.startfile(os.path.abspath(archivo_pdf))
        
    def obtener_numero_factura_actual(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("SELECT MAX(factura) FROM Ventas")
            max_factura = c.fetchone()[0]
            if max_factura:
                return max_factura +1
            else:
                return 1
        except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al obtener el numero de factura: {e}")
                return 1
        finally:
            conn.close()

    def mostrar_numero_factura(self):
        self.num_factura.set(self.numero_factura_actual)

    def abrir_ventana_factura(self):
        ventana_facturas = Toplevel()
        ventana_facturas.title("Facutras")
        ventana_facturas.geometry("800x500")
        ventana_facturas.config(bg="#8258FA")
        ventana_facturas.resizable(False, False)

        facturas = Label(ventana_facturas, bg="#8181F7", text="Facturas registradas", font="Helvetica 36")
        facturas.place(x=150, y=15)

        treeFrame = tk.Frame(ventana_facturas, bg="#8181F7")
        treeFrame.place(x=10, y=100, width=780, height=380)

        scroll_y = ttk.Scrollbar(treeFrame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = ttk.Scrollbar(treeFrame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        tree_facturas = ttk.Treeview(treeFrame, columns=("ID", "Factura", "Producto", "Precio", "Cantidad", "Subtotal"), show="headings", height=10, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=tree_facturas.yview)
        scroll_x.config(command=tree_facturas.xview)
        
        tree_facturas.heading("#1", text="ID")
        tree_facturas.heading("#2", text="Factura")
        tree_facturas.heading("#3", text="Producto")
        tree_facturas.heading("#4", text="Precio")
        tree_facturas.heading("#4", text="Cantidad")
        tree_facturas.heading("#4", text="Subtotal")
        
        tree_facturas.column("ID", width=70, anchor="center")
        tree_facturas.column("Factura", width=100, anchor="center")
        tree_facturas.column("Producto", width=200, anchor="center")
        tree_facturas.column("Precio", width=130, anchor="center")
        tree_facturas.column("Cantidad", width=130, anchor="center")
        tree_facturas.column("Subtotal", width=130, anchor="center")

        tree_facturas.pack(expand=True, fill=BOTH)    

        self.cargar_facturas(tree_facturas)        

    def cargar_facturas(self, tree):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM Ventas")
            facturas = c.fetchall()
            for factura in facturas:
                tree.insert("","end", values=factura)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar las facturas: {e}")
