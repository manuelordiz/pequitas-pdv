import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

class Clientes(tk.Frame):
    db_name = "database.db"
    
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.widgets()

    def widgets(self):
        # Frame para título
        frame1 = tk.Frame(self, bg="#8258FA", highlightbackground="gray", highlightthickness=1)
        frame1.place(x=0, y=0, width=1110, height=100)
        
        titulo = tk.Label(self, text="Clientes", bg="#8258FA", font="Helvetica 24 bold", anchor="center")
        titulo.place(x=5, y=0, width=1090, height=90)
        
        # Frame para formulario y botones
        frame2 = tk.Frame(self, bg="#8181F7", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)

        labelframe = LabelFrame(frame2, text="Clientes", font="Helvetica 22", bg="#8181F7")
        labelframe.place(x=20, y=30, width=400, height=500)
        
        lbl_nombre = tk.Label(labelframe, text="Nombre: ", font="Helvetica 16", bg="#8181F7")
        lbl_nombre.place(x=10, y=20)
        self.nombre = ttk.Entry(labelframe, font="Helvetica 12")
        self.nombre.place(x=140, y=20, width=240, height=40)
        
        lbl_apellido = tk.Label(labelframe, text="Apellido: ", font="Helvetica 16", bg="#8181F7")
        lbl_apellido.place(x=10, y=80)
        self.apellido = ttk.Entry(labelframe, font="Helvetica 12")
        self.apellido.place(x=140, y=80, width=240, height=40)
        
        lbl_telefono = tk.Label(labelframe, text="Telefono: ", font="Helvetica 16", bg="#8181F7")
        lbl_telefono.place(x=10, y=140)
        self.telefono = ttk.Entry(labelframe, font="Helvetica 12")
        self.telefono.place(x=140, y=140, width=240, height=40)
        
        lbl_direccion = tk.Label(labelframe, text="Direccion: ", font="Helvetica 16", bg="#8181F7")
        lbl_direccion.place(x=10, y=200)
        self.direccion = ttk.Entry(labelframe, font="Helvetica 12")
        self.direccion.place(x=140, y=200, width=240, height=40)
        
        lbl_saldo = tk.Label(labelframe, text="Saldo: ", font="Helvetica 16", bg="#8181F7")
        lbl_saldo.place(x=10, y=260)
        self.saldo = ttk.Entry(labelframe, font="Helvetica 12")
        self.saldo.place(x=140, y=260, width=240, height=40)
        
        btn_agregar = tk.Button(labelframe, text="Agregar", font="Helvetica 16", bg="#BDBDBD", command=self.registrar)
        btn_agregar.place(x=80, y=340, width=240, height=40)
        
        btn_editar = tk.Button(labelframe, text="Modificar", font="Helvetica 16", bg="#BDBDBD", command=self.editar_cliente)
        btn_editar.place(x=80, y=400, width=240, height=40)
        
        # Treeview para mostrar clientes
        treeframe = tk.Frame(frame2, bg="white")
        treeframe.place(x=440, y=55, width=620, height=400)
        
        scroll_y = ttk.Scrollbar(treeframe)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scroll_x = ttk.Scrollbar(treeframe, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree = ttk.Treeview(treeframe, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, height=15,
                                 columns=("ID", "Nombre", "Apellido", "Telefono", "Direccion", "Saldo"), show="headings")
        self.tree.pack(expand=True, fill=tk.BOTH)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Telefono", text="Telefono")
        self.tree.heading("Direccion", text="Direccion")
        self.tree.heading("Saldo", text="Saldo")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=120, anchor="center")
        self.tree.column("Apellido", width=120, anchor="center")
        self.tree.column("Telefono", width=100, anchor="center")
        self.tree.column("Direccion", width=150, anchor="center")
        self.tree.column("Saldo", width=70, anchor="center")

        self.mostrar_clientes()

        btn_actualizar = tk.Button(frame2, text="Actualizar lista", font="Helvetica 14", bg="#BDBDBD", command=self.actualizar_lista)
        btn_actualizar.place(x=440, y=480, width=240, height=40)
        
        btn_eliminar = tk.Button(frame2, text="Eliminar cliente", font="Helvetica 14", bg="#BDBDBD", command=self.eliminar_cliente)
        btn_eliminar.place(x=700, y=480, width=240, height=40)

    def ejecutar_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(consulta, parametros)
            conn.commit()
        return result

    def validar_datos(self, nombre, apellido, telefono, direccion, saldo):
        if not (nombre and apellido and telefono and direccion and saldo):
            return False
        try:
            int(telefono)
            float(saldo)  # Permitir decimales en saldo
        except ValueError:
            return False
        return True
    
    def mostrar_clientes(self):
        consulta = "SELECT * FROM clientes ORDER BY id DESC"
        result = self.ejecutar_consulta(consulta)
        for row in result:
            self.tree.insert("", 0, values=row)

    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.mostrar_clientes()
        messagebox.showinfo("Actualización", "La lista de clientes se ha actualizado correctamente.")

    def registrar(self):
        nombre = self.nombre.get()
        apellido = self.apellido.get()
        telefono = self.telefono.get()
        direccion = self.direccion.get()
        saldo = self.saldo.get()
        
        if self.validar_datos(nombre, apellido, telefono, direccion, saldo):
            try:
                consulta = "INSERT INTO clientes VALUES(NULL, ?, ?, ?, ?, ?)"
                parametros = (nombre, apellido, telefono, direccion, saldo)
                self.ejecutar_consulta(consulta, parametros)
                self.actualizar_lista()
                self.nombre.delete(0, tk.END)
                self.apellido.delete(0, tk.END)
                self.telefono.delete(0, tk.END)
                self.direccion.delete(0, tk.END)
                self.saldo.delete(0, tk.END)
            except Exception as e:
                messagebox.showwarning("Error", f"Error al registrar el cliente: {e}")
        else:
            messagebox.showwarning("Error", "Por favor, rellene todos los campos correctamente.")

    def editar_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Editar Cliente", "Seleccione un cliente para editar.")
            return

        item_id = self.tree.item(seleccion)["values"][0]

        ventana_editar = tk.Toplevel(self)
        ventana_editar.title("Editar Cliente")
        ventana_editar.geometry("500x450")
        
        lbl_nombre = tk.Label(ventana_editar, text="Nombre:", font="Helvetica 14")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = ttk.Entry(ventana_editar, font="Helvetica 12")
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        lbl_apellido = tk.Label(ventana_editar, text="Apellido:", font="Helvetica 14")
        lbl_apellido.grid(row=1, column=0, padx=10, pady=10)
        entry_apellido = ttk.Entry(ventana_editar, font="Helvetica 12")
        entry_apellido.grid(row=1, column=1, padx=10, pady=10)

        lbl_telefono = tk.Label(ventana_editar, text="Teléfono:", font="Helvetica 14")
        lbl_telefono.grid(row=2, column=0, padx=10, pady=10)
        entry_telefono = ttk.Entry(ventana_editar, font="Helvetica 12")
        entry_telefono.grid(row=2, column=1, padx=10, pady=10)

        lbl_direccion = tk.Label(ventana_editar, text="Dirección:", font="Helvetica 14")
        lbl_direccion.grid(row=3, column=0, padx=10, pady=10)
        entry_direccion = ttk.Entry(ventana_editar, font="Helvetica 12")
        entry_direccion.grid(row=3, column=1, padx=10, pady=10)

        lbl_saldo = tk.Label(ventana_editar, text="Saldo:", font="Helvetica 14")
        lbl_saldo.grid(row=4, column=0, padx=10, pady=10)
        entry_saldo = ttk.Entry(ventana_editar, font="Helvetica 12")
        entry_saldo.grid(row=4, column=1, padx=10, pady=10)

        def guardar_cambios():
            nombre = entry_nombre.get()
            apellido = entry_apellido.get()
            telefono = entry_telefono.get()
            direccion = entry_direccion.get()
            saldo = entry_saldo.get()

            if self.validar_datos(nombre, apellido, telefono, direccion, saldo):
                try:
                    consulta = "UPDATE clientes SET nombre=?, apellido=?, telefono=?, direccion=?, saldo=? WHERE id=?"
                    parametros = (nombre, apellido, telefono, direccion, saldo, item_id)
                    self.ejecutar_consulta(consulta, parametros)
                    self.actualizar_lista()
                    ventana_editar.destroy()
                except Exception as e:
                    messagebox.showwarning("Error", f"Error al actualizar el cliente: {e}")
            else:
                messagebox.showwarning("Error", "Por favor, rellene todos los campos correctamente.")

        btn_guardar = tk.Button(ventana_editar, text="Guardar Cambios", bg="#BDBDBD", font="Helvetica 14", command=guardar_cambios)
        btn_guardar.place(x=125, y=350, width=200, height=40)

    def eliminar_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Eliminar Cliente", "Seleccione un cliente para eliminar.")
            return
        
        if messagebox.askyesno("Eliminar Cliente", "¿Está seguro que desea eliminar este cliente?"):
            item_id = self.tree.item(seleccion)["values"][0]
            consulta = "DELETE FROM clientes WHERE id=?"
            self.ejecutar_consulta(consulta, (item_id,))
            self.actualizar_lista()