from tkinter import *
from tkinter import ttk

class Application():
    def __init__(self):
        self.root = Tk()
        self.root.title('SolutionPy')     
        self.root.iconbitmap('Image/Chart.ico')
        self.root.config(bg='#e5e7e9')
        self.root.state('zoomed')

    def create_widgets(self):
        #Menu=ttk.Notebook(self.root)
        s =ttk.Style()
        s.theme_use('default')
        s.configure('TNotebook', tabposition='n',background='#17202a') 
        s.configure('TNotebook.Tab', font=('Segoe UI', 12,'bold'),background='#3498db', foreground='white', borderwidth=0)
        s.map('TNotebook.Tab', background=[('selected', '#2471a3'),('active', "#3498db")], foreground=[("selected", 'white')])
        #s.theme_use("default")
        
    
        #Menu.styl
        #Menu.config(width=2000,height=1000)
        #Ventana_Cargar=CargarArchivo(Menu)
        #Ventana_Analizar=AnalizarArchivo(Menu)
        #Ventana_Reportes=VerReportes(Menu)
        #Ventana_VerImagen=VerImagen(Menu)
        #Menu.add(Ventana_Cargar.FrameCargar,text='Cargar Archivo',padding=10)
        #Menu.add(Ventana_Analizar.FrameAnalizar,text="Analizar Archivo", padding=10)
        #Menu.add(Ventana_VerImagen.FrameVerImagen,text="Ver Imagen", padding=10)
        #Menu.add(Ventana_Reportes.FrameReportes,text="Ver Reportes", padding=10)

        
        #fill='both', expand=True
        #Menu.pack(ipadx=10,ipady=10,expand=True)
        


    def say_hi(self):
        pass
        #os.system('dot -Tpng imagen.html -o NuevaImagen.png')


Aps=Application()
Aps.create_widgets()
Aps.root.mainloop()