from tkinter import *
from tkinter import ttk

class Application():
    def __init__(self):
        self.root = Tk()
        self.root.title('SolutionPy')     
        self.root.iconbitmap('Image/Chart.ico')
        self.root.config(bg='#f0f3f4')
        self.root.state('zoomed')

    def create_widgets(self):
        #Menu=ttk.Notebook(self.root)
        s =ttk.Style()
        labelframe = LabelFrame(self.root, text="Opciones",bg = "#212f3d",bd=1,labelanchor='n',fg='white')
        labelframe.pack(ipadx=50,ipady=50)
        labelframe.config(font=('Segoe UI', 20,'bold'))
        #labelframe.pack(expand=True,fill=X,pady=100)
        labelframe.place(x=40,y=20,width=1260,height=100)
        ##
        self.ButtonAbrirArchivo=Button(labelframe,text='Cargar Archivo',font=('Segoe UI', 12),bd=0,pady=10,padx=10,bg='#f7f9f9',fg='black')
        self.ButtonAbrirArchivo.place(x=400, y=10,width=150,height=30)

        self.ButtonCargarArchivo=Button(labelframe,text ="Analizar Archivo",font=('Segoe UI', 12),bd=0,pady=10,padx=10,bg='#f7f9f9',fg='black')
        self.ButtonCargarArchivo.place(x=600, y=10,width=150,height=30)
        
        self.combo=ttk.Combobox(labelframe,state="readonly")
        self.combo.place(x=800, y=10,width=150,height=30)


        ##
        self.text2 = Text(self.root, height=20, width=50)
        scroll = Scrollbar(self.root, command=self.text2.yview)
        self.text2.configure(yscrollcommand=scroll.set,bg='#fdfefe',foreground='black',font=('Segoe UI', 12,))
        #self.text2.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
       
        #self.text2.insert(END, quote)
        self.text2.place(x=40, y=150,width=800,height=540)
        ##
        self.TextConsola=Text (self.root, height=20, width=50)   
        scrollConsola=Scrollbar(self.root,command=self.TextConsola.yview)
        self.TextConsola.configure(yscrollcommand=scrollConsola.set,state=NORMAL,background='#000000',font=('Segoe UI', 12,),foreground='white',insertbackground='white')
        self.TextConsola.place(x=900, y=150,width=400,height=540)

        scrollConsola.pack(expand=True,padx=10, fill=Y)
        scrollConsola.place(x=1290,y=150,height=540)
        ##
        scroll.pack(expand=True,padx=10, fill=Y)
        scroll.place(x=823,y=150,height=540)
        
        
    
        
        


    def say_hi(self):
        pass
        #
        #


Aps=Application()
Aps.create_widgets()
Aps.root.mainloop()