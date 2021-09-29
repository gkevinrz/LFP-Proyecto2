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
        
        labelframe = LabelFrame(self.root, text="Opciones",bg = "#2c3e50",bd=3,labelanchor='n',fg='white')
        
        labelframe.config(font=('Segoe UI', 20,'bold'))
        labelframe.place(x=40, y=20,width=400,height=90)
        
        text2 = Text(self.root, height=20, width=50)
        scroll = Scrollbar(self.root, command=text2.yview)
        text2.configure(yscrollcommand=scroll.set)
        text2.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
        text2.tag_configure('big', font=('Verdana', 20, 'bold'))
        text2.tag_configure('color',
                    foreground='#476042',
                    font=('Tempus Sans ITC', 12, 'bold'))
        text2.tag_bind('follow',
               '<1>',
               lambda e, t=text2: t.insert(END, "Not now, maybe later!"))
        text2.insert(END,'\nWilliam Shakespeare\n', 'big')
        quote = """
            To be, or not to be that is the question:
            Whether 'tis Nobler in the mind to suffer
            The Slings and Arrows of outrageous Fortune,
            Or to take Arms against a Sea of troubles,
            """
        text2.insert(END, quote, 'color')
        text2.insert(END, 'follow-up\n', 'follow')
        text2.place(x=40, y=150,width=800,height=500)

        scroll.pack(expand=True,padx=10, fill=Y)
        scroll.place(x=823,y=150,height=500)
        
        
        
        
        
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