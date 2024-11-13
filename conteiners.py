from tkinter import *
import tkinter as tk
from ventas import Ventas
from inventario import Inventario
from clientes import Clientes
from aboutus import Info
from PIL import Image, ImageTk

class Container(tk.Frame):
    def __init__(self, padre, contenedor):
        super().__init__(padre)
        self.contenedor = contenedor
        self.pack()
        self.place(x=0, y=0, width=800, height=600)
        self.config(bg="#F6D8CE")
        self.widgets()
        
    def show_frames(self, container):
        top_level = tk.Toplevel(self)
        frame = container(top_level)
        frame.config(bg="#E0F2F7")
        frame.pack(fill="both", expand=True)
        top_level.geometry("1100x650+120+20")
        top_level.resizable(False, False)

        top_level.transient(self.master)
        top_level.grab_set()
        top_level.focus_set()
        top_level.lift()
        
        

    def ventas(self):
        self.show_frames(Ventas)
        
    def inventario(self):
        self.show_frames(Inventario)

    def clientes(self):
        self.show_frames(Clientes)

    def informacion(self):
        self.show_frames(Info)
        
    def widgets(self):
        
        frame1 = tk.Frame(self, bg="#8181F7")
        frame1.pack()
        frame1.place(x=0, y=0, width=800, height=600)
        
        btn_ventas = Button(frame1, bg="#BDBDBD", fg="black", text="Ventas", font="Helvetica 18", command=self.ventas)
        btn_ventas.place(x=500, y=30, width=240, height=60)
        
        btn_inventario = Button(frame1, bg="#BDBDBD", fg="black", text="Inventario", font="Helvetica 18", command=self.inventario)
        btn_inventario.place(x=500, y=130, width=240, height=60)

        btn_clientes = Button(frame1, bg="#BDBDBD", fg="black", text="Clientes", font="Helvetica 18", command=self.clientes)
        btn_clientes.place(x=500, y=230, width=240, height=60)
        
        btn_info = Button(frame1, bg="#BDBDBD", fg="black", text="Sobre Nosotros", font="Helvetica 18", command=self.informacion)
        btn_info.place(x=500, y=330, width=240, height=60)
        
        self.logo_imagen = Image.open("store.png")
        self.logo_imagen = self.logo_imagen.resize((365,365))
        self.logo_imagen = ImageTk.PhotoImage(self.logo_imagen)
        self.logo_label = tk.Label(frame1, image=self.logo_imagen, bg="#8181F7")
        self.logo_label.place(x=50, y=30)
       
        
        