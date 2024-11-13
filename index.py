from tkinter import Tk, Frame
from conteiners import Container
from ttkthemes import ThemedStyle


class Inicio(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Stock Manager")
        self.resizable(False, False)
        self.configure(bg="#8181F7")
        self.geometry("800x600+120+20") 
        #self.iconbitmap("store1.ico")
        
        
        self.container = Frame(self, bg="#8181F7")
        self.container.pack(fill="both", expand=True)
        
        self.frames = {
            Container: None
        }
        
        self.load_frame()
        
        self.show_frames(Container)

        self.set_theme()
        
    def load_frame(self):
        for FrameClass in self.frames.keys():
            Frame = FrameClass(self.container, self)
            self.frames[FrameClass] = Frame
            
    def show_frames(self, FrameClass):
        frame = self.frames[FrameClass]
        frame.tkraise()
        
    def set_theme(self):
        style = ThemedStyle(self)
        style.set_theme("breeze")
        



def main():
    app = Inicio()
    app.mainloop
    
if __name__ == "__main__":
    main()