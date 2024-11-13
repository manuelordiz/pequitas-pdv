import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

class Inventario(tk.Frame):
    db_name = "database.db"

    def __init__(self, padre):
        super().__init__(padre)
        self.pack()
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.widgets()
        
    def widgets(self):
        
        frame1 = tk.Frame(self, bg="#8258FA", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1110, height=100)
        
        titulo = tk.Label(self, text="Inventario", bg="#8258FA", font="Helvetica 24 bold", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)
        
        frame2 = tk.Frame(self, bg="#8181F7", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)
        
        #Agregado modificacion productos
        
        labelframe = LabelFrame(frame2, text="Productos", font="Helvetica 22", bg="#8181F7")
        labelframe.place(x=20, y=30, width=400, height=500)
        
        lbl_nombre = Label(labelframe, text="Nombre: ", font="Helvetica 16", bg="#8181F7")
        lbl_nombre.place(x=10, y=20)
        self.nombre = ttk.Entry(labelframe, font="Helvetica 12")
        self.nombre.place(x=140, y=20, width=240, height=40)
        
        lbl_proveedor = Label(labelframe, text="Prooveedor: ", font="Poppis 16", bg="#8181F7")
        lbl_proveedor.place(x=10, y=80)
        self.proveedor = ttk.Entry(labelframe, font="Helvetica 12")
        self.proveedor.place(x=140, y=80, width=240, height=40)
        
        lbl_precio = Label(labelframe, text="Precio: ", font="Helvetica 16", bg="#8181F7")
        lbl_precio.place(x=10, y=140)
        self.precio = ttk.Entry(labelframe, font="Helvetica 12")
        self.precio.place(x=140, y=140, width=240, height=40)
        
        lbl_costo = Label(labelframe, text="Costo: ", font="Helvetica 16", bg="#8181F7")
        lbl_costo.place(x=10, y=200)
        self.costo = ttk.Entry(labelframe, font="Helvetica 12")
        self.costo.place(x=140, y=200, width=240, height=40)
        
        lbl_stock = Label(labelframe, text="Stock: ", font="Helvetica 16", bg="#8181F7")
        lbl_stock.place(x=10, y=260)
        self.stock = ttk.Entry(labelframe, font="Helvetica 12")
        self.stock.place(x=140, y=260, width=240, height=40)
        
        btn_agregar = tk.Button(labelframe, text="Agregar", font="Helvetica 16", bg="#BDBDBD", command=self.registrar)
        btn_agregar.place(x=80, y=340, width=240, height=40)
        
        btn_editar = tk.Button(labelframe, text="Modificar", font="Helvetica 16", bg="#BDBDBD", command=self.editar_producto)
        btn_editar.place(x=80, y=400, width=240, height=40)
        
        #Table
        
        treeframe = Frame(frame2, bg="white")
        treeframe.place(x=440, y=55, width=620, height=400)
        
        scroll_y = ttk.Scrollbar(treeframe)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = ttk.Scrollbar(treeframe, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        self.tree = ttk.Treeview(treeframe, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, height=40, columns=("ID", "PRODUCTO", "PROVEEDOR", "PRECIO", "COSTO", "STOCK"), show="headings" )
        self.tree.pack(expand=True, fill=BOTH)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        self.tree.heading("ID", text="Id")
        self.tree.heading("PRODUCTO", text="Producto")
        self.tree.heading("PROVEEDOR", text="Proveedor")
        self.tree.heading("PRECIO", text="Precio")
        self.tree.heading("COSTO", text="Costo")
        self.tree.heading("STOCK", text="Stock")
        
        self.tree.column("ID", width=70, anchor="center")
        self.tree.column("PRODUCTO", width=100, anchor="center")
        self.tree.column("PROVEEDOR", width=100, anchor="center")
        self.tree.column("PRECIO", width=100, anchor="center")
        self.tree.column("COSTO", width=100, anchor="center")
        self.tree.column("STOCK", width=70, anchor="center")

        self.mostrar()

        btn_actualizar = Button(frame2, text="Actualizar inventario", font="Helvetica 14", bg="#BDBDBD", command=self.actualizar_inventario)
        btn_actualizar.place(x=440, y=480, width=240, height=40)
        
        btn_eliminiar = Button(frame2, text="Eliminar producto", font="Helvetica 14", bg="#BDBDBD", command=self.eliminar_producto)
        btn_eliminiar.place(x=700, y=480, width=240, height=40)

    def eje_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(consulta, parametros)
            conn.commit()
        return result

    def validacion(self, nombre, prov, precio, costo, stock):
        if not (nombre, prov, precio, costo, stock):
            return False
        try:
            float(precio)
            float(costo)
            int(stock)
        except ValueError:
            return False
        return True
    
    def mostrar(self):
        consulta = "SELECT * FROM inventario ORDER BY id DESC"
        result = self.eje_consulta(consulta)
        for elem in result:
            try:
                precio = float(elem[3]) 
                costo = float(elem[4]) 
            except ValueError:
                precio = elem[3]
                costo = elem[4]
            self.tree.insert("", 0, text=elem[0], values=(elem[0], elem[1], elem[2], precio, costo, elem[5]))

    def actualizar_inventario(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.mostrar()

        messagebox.showinfo("Actualizacion", "El inventario ha sido actualizado.")
        
        
    def registrar(self):
        result = self.tree.get_children()
        for i in result:
            self.tree.delete(i)
        nombre = self.nombre.get()
        prov = self.proveedor.get()
        precio = self.precio.get()
        costo = self.costo.get()
        stock = self.stock.get()
        if self.validacion(nombre, prov, precio, costo, stock):
            try:
                consulta = "INSERT INTO inventario VALUES(?,?,?,?,?,?)"
                parametros = (None, nombre, prov, precio, costo, stock)
                self.eje_consulta(consulta, parametros)
                self.mostrar()
                self.nombre.delete(0, END)
                self.proveedor.delete(0, END)
                self.precio.delete(0, END)
                self.costo.delete(0, END)
                self.stock.delete(0, END)
            except Exception as e:
                messagebox.showwarning(title="Error", message=f"Error al registrar eL producto: {e}")
        else:
            messagebox.showwarning(title="Error", message="Rellene todos los campos correctamente")
            self.mostrar()

    def editar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Editar Producto", "Seleccione un producto para editar")
            return

        item_id = self.tree.item(seleccion)["text"]
        item_values = self.tree.item(seleccion)["values"]

        ventana_editar = Toplevel(self)
        ventana_editar.title("Editar Producto")
        ventana_editar.geometry("400x400")
        ventana_editar.config(bg="#8258FA")

        lbl_nombre = Label(ventana_editar, text="Nombre: ", font="Helvetica 14", bg="#8181F7")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = Entry(ventana_editar, font="Helvetica 12")
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        entry_nombre.insert(0, item_values[1])

        lbl_proveedor = Label(ventana_editar, text="Proveedor: ", font="Helvetica 14", bg="#8181F7")
        lbl_proveedor.grid(row=1, column=0, padx=10, pady=10)
        entry_proveedor = Entry(ventana_editar, font="Helvetica 12")
        entry_proveedor.grid(row=1, column=1, padx=10, pady=10)
        entry_proveedor.insert(0, item_values[2])

        lbl_precio = Label(ventana_editar, text="Precio: ", font="Helvetica 14", bg="#8181F7")
        lbl_precio.grid(row=2, column=0, padx=10, pady=10)
        entry_precio = Entry(ventana_editar, font="Helvetica 12")
        entry_precio.grid(row=2, column=1, padx=10, pady=10)
        entry_precio.insert(0, item_values[3])

        lbl_costo = Label(ventana_editar, text="Costo: ", font="Helvetica 14", bg="#8181F7")
        lbl_costo.grid(row=3, column=0, padx=10, pady=10)
        entry_costo = Entry(ventana_editar, font="Helvetica 12")
        entry_costo.grid(row=3, column=1, padx=10, pady=10)
        entry_costo.insert(0, item_values[4])

        lbl_stock = Label(ventana_editar, text="Stock: ", font="Helvetica 14", bg="#8181F7")
        lbl_stock.grid(row=4, column=0, padx=10, pady=10)
        entry_stock = Entry(ventana_editar, font="Helvetica 12")
        entry_stock.grid(row=4, column=1, padx=10, pady=10)
        entry_stock.insert(0, item_values[5])

        def guardar_cambios():
            nombre = entry_nombre.get()
            proveedor = entry_proveedor.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()

            if not (nombre and proveedor and precio and costo and stock):
                messagebox.showwarning("Guardar Cambios", "Rellene todos los campos")
                return
            try:
                precio = float(precio.replace(",", ""))
                costo = float(costo.replace(",", ""))
            except ValueError:
                messagebox.showwarning("Guardar Cambios", "Ingrese valores numericos validos para precio y costo")
                return
            
            consulta = "UPDATE inventario SET nombre=?, proveedor=?, precio=?, costo=?, stock=? WHERE id=?"
            parametros = (nombre, proveedor, precio, costo, stock, item_id)
            self.eje_consulta(consulta, parametros)

            self.actualizar_inventario()

            ventana_editar.destroy()
        
        btn_guardar = Button(ventana_editar, text="Guardar Cambios", bg="#BDBDBD", font="Poppis 14", command=guardar_cambios)
        btn_guardar.place(x=80, y=250, width=240, height=40)  
        
    def eliminar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Eliminar Producto", "Seleccione un producto para eliminar")
            return
        
        if messagebox.askyesno("Eliminar Producto", "¿Está seguro que desea eliminar este producto?"):
            item_id = self.tree.item(seleccion)["text"]
            consulta = "DELETE FROM inventario WHERE id=?"
            self.eje_consulta(consulta, (item_id,))
            self.actualizar_inventario()