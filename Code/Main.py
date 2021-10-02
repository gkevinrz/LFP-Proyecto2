from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

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
        self.ButtonAbrirArchivo=Button(labelframe,text='Cargar Archivo',font=('Segoe UI', 12),bd=0,pady=10,padx=10,bg='#f7f9f9',fg='black',command=self.select_file)
        self.ButtonAbrirArchivo.place(x=400, y=10,width=150,height=30)

        self.ButtonAnalizarArchivo=Button(labelframe,text ="Analizar Archivo",font=('Segoe UI', 12),bd=0,pady=10,padx=10,bg='#f7f9f9',fg='black')
        self.ButtonAnalizarArchivo.place(x=600, y=10,width=150,height=30)
        
        self.combo=ttk.Combobox(labelframe,state="readonly")
        self.combo.place(x=800, y=10,width=230,height=30)
        self.combo.config(font=('Segoe UI', 12,))
        self.combo['values']=['Generar Reporte de Errores','Generar Reporte de Tokens','Generar Árbol de derivación']
        
        ##
        self.TextoEntrada = Text(self.root, height=20, width=50)
        scroll = Scrollbar(self.root, command=self.TextoEntrada.yview)
        self.TextoEntrada.configure(yscrollcommand=scroll.set,bg='#fdfefe',foreground='black',font=('Segoe UI', 12,))
        self.TextoEntrada.place(x=40, y=150,width=800,height=540)
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


    def select_file(self):
        filetypes = (('Archivos lfp', '*.lfp'),('Todos los archivos', '*.*'))
        archivo = filedialog.askopenfile(title='Abrir un archivo',initialdir='./',filetypes=filetypes)
        if archivo is None:
            messagebox.showerror(title='Error', message='No se eligió ningún archivo')
            return None
        else:
            texto = archivo.read()
            archivo.close()
            messagebox.showinfo(title='Información', message='Archivo cargado exitosamente')
            self.TextoEntrada.insert(END,texto)



    def Lectura(self):
        if self.TextoEntrada is not None:
            #print(textoanalizar)
            self.TextoEntrada+= "~"
            messagebox.showinfo(title='Información', message='Lectura exitosa')
            self.Analizar(self.TextoEntrada)
            #print(self.TextoEntrada)
        else:
            messagebox.showerror(title='Error', message='No se pudo analizar la entrada, intenta de nuevo')
        
        
    

    def Generar_TablaTokens(self):
        pass
        #
        #
    def Generar_TablaErrores(self):
        pass

    def Generar_Arbol(self):
        pass






Aps=Application()
Aps.create_widgets()
Aps.root.mainloop()