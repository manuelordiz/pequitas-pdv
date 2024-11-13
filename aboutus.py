from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

class Info(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()

    def widgets(self):
        
        frame1 = tk.Frame(self, bg="#8258FA", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1110, height=100)
        
        titulo = tk.Label(self, text="Sobre Nosotros", bg="#8258FA", font="Helvetica 24 bold", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)
        
        frame2 = tk.Frame(self, bg="#8181F7", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)

        labelframe = LabelFrame(frame2, text="Sobre Nosotros", font="Helvetica 22", bg="#8181F7")
        labelframe.place(x=20, y=30, width=1090, height=450)
        
        label_copy = tk.Label(labelframe, text="Copyright (c) 2024 Manuel Ordiz\n All Rights Reserved\n This product is protected by copyright and distributed under \nlicenses restricting copying, distribution, and decompilation.",
                              font="Helvetica 16", bg="#8181F7", anchor="center")
        label_copy.place(x=25, y=40)
        
        lbl_img = tk.Label(labelframe, text="Image Designed by catalyststuff / Freepik", font="helvetica 16", bg="#8181F7")
        lbl_img.place(x=20, y=150)