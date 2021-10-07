from os import lseek
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from Error import Error
from Token import Token

class Application():
    def __init__(self):
        self.root = Tk()
        self.root.title('SolutionPy')     
        self.root.iconbitmap('Image/Chart.ico')
        self.root.config(bg='#f0f3f4')
        self.root.state('zoomed')
        self.text=''
        self.ListaErrores1=[]
        self.ListaTokens1=[]
        self.ListaErrores=[]
        self.ListaTokens=[]

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

        self.ButtonAnalizarArchivo=Button(labelframe,text ="Analizar Archivo",font=('Segoe UI', 12),bd=0,pady=10,padx=10,bg='#f7f9f9',fg='black',command=self.Lectura)
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
        self.combo.bind('<<ComboboxSelected>>', self.AccionComboBox)

    def select_file(self):
        filetypes = (('Archivos lfp', '*.lfp'),('Todos los archivos', '*.*'))
        archivo = filedialog.askopenfile(title='Abrir un archivo',initialdir='./',filetypes=filetypes)
        if archivo is None:
            messagebox.showerror(title='Error', message='No se eligió ningún archivo')
            return None
        else:
            self.text = archivo.read()
            archivo.close()
            messagebox.showinfo(title='Información', message='Archivo cargado exitosamente')
            self.TextoEntrada.insert(INSERT,self.text)



    def Lectura(self):
        TextoAnalisis=self.TextoEntrada.get('1.0','end-1c')
        if TextoAnalisis.isspace() or self.TextoEntrada.get('1.0','end-1c')=='':
            messagebox.showerror(title='Error', message='No se pudo analizar la entrada, intenta de nuevo')
        else:
            messagebox.showinfo(title='Información', message='Lectura exitosa')
            TextoAnalizar=self.TextoEntrada.get('1.0','end-1c')
            #print(TextoAnalizar)
            self.AnalisisLexico(TextoAnalizar)
            TextoAnalizar=''



        #TextoAnalizar=self.TextoEntrada.get('1.0','end-1c')
        #if TextoAnalizar is not None:
        #    print(TextoAnalizar)
            #self.TextoEntrada+= "~"
        #    messagebox.showinfo(title='Información', message='Lectura exitosa')
            #self.Analizar(self.TextoEntrada)
            #print(self.TextoEntrada)
        #elif TextoAnalizar=='':
        #    messagebox.showerror(title='Error', message='No se pudo analizar la entrada, intenta de nuevo')
        
    

    def isLetra(self,caracter):
        if((ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122) or ord(caracter) == 164 or ord(caracter) == 165):
            return True
        else:
            return False

    def isNumero(self,caracter):
        if ((ord(caracter) >= 48 and ord(caracter) <= 57)):
            return True
        else:
            return False
    def isSimbolo(self,caracter):
        if ((ord(caracter)==61) or (ord(caracter)==123) or (ord(caracter)==125) or (ord(caracter)==91) or (ord(caracter)==93) or (ord(caracter)==44) or (ord(caracter)==40) or (ord(caracter)==41) or (ord(caracter)==59)):
            return True
        else:
            return False
    

    def AnalisisLexico(self,Texto):
        contador=0
        fila = 1
        columna = 0
        estado=0
        Tk_Identificador=''
        Tk_Simbolo=''
        Tk_ComillasDobles=''
        Tk_ComillaSimple=''
        Tk_Numeral=''
        Tk_Numero=''
        Tk_Cadena=''
        Texto=Texto+'~'
        for c in Texto:
            if estado==0:
                if self.isLetra(c):
                    Tk_Identificador=Tk_Identificador+c
                    estado=1
                elif self.isSimbolo(c):
                    Tk_Simbolo=c
                    estado=2
                    contador+=1
                    token=Token(contador,Tk_Simbolo,fila,str(columna - (len(Tk_Simbolo) - 1)),'Simbolo')
                    self.ListaTokens1.append(token)
                    Tk_Simbolo=''
                elif ord(c)==34:
                    Tk_ComillasDobles=Tk_ComillasDobles+c
                    contador+=1
                    token=Token(contador,Tk_ComillasDobles,fila,str(columna - (len(Tk_ComillasDobles) - 1)),'Comillas Dobles')
                    self.ListaTokens1.append(token)
                    Tk_ComillasDobles=''
                    estado=3
                #elif ((ord(c)==43) or (ord(c)==45)):
                    #lexActual=lexActual+c
                    #estado=5
                #elif self.isNumero(c):
                    #lexActual=lexActual+c
                    #estado=6
                #elif ord(c)==35:
                    #lexActual=lexActual+c
                    #estado=9    
                #elif ord(c)==39:
                    #lexActual=lexActual+c
                    #estado=10
                else:
                    if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                        pass
                    else:
                        error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error)
            elif estado==1:
                if self.isNumero(c):
                    Tk_Identificador=Tk_Identificador+c
                    estado=1
                elif self.isLetra(c):
                    Tk_Identificador=Tk_Identificador+c
                    estado=1
                elif ord(c)==95:
                    Tk_Identificador=Tk_Identificador+c
                    estado=1
                else:
                    contador+=1
                    token=Token(contador,Tk_Identificador,fila,str(columna - (len(Tk_Identificador) - 1)),'Palabra Reservada')
                    self.ListaTokens1.append(token)
                    Tk_Identificador=''
                    if self.isSimbolo(c):
                        Tk_Simbolo=Tk_Simbolo+c
                        contador+=1
                        token=Token(contador,Tk_Simbolo,fila,columna - (len(Tk_Simbolo)),'Simbolo')
                        self.ListaTokens1.append(token)
                        Tk_Simbolo=''
                        estado=0 #PENDIENTE
                        continue
                    elif self.isLetra(c):
                        Tk_Identificador=Tk_Identificador+c
                        estado=1
                        continue
                    elif ord(c)==34:
                        Tk_ComillasDobles=Tk_ComillasDobles+c
                        contador+=1
                        token=Token(contador,Tk_ComillasDobles,fila,str(columna - (len(Tk_ComillasDobles))),'Comillas Dobles')
                        self.ListaTokens1.append(token)
                        Tk_ComillasDobles=''
                        estado=3
                        continue
                    elif ((ord(c)==43) or (ord(c)==45)):
                        Tk_Numero=Tk_Numero+c
                        estado=5
                        continue
                    elif self.isNumero(c):
                        lexActual=lexActual+c
                        estado=6
                        continue
                    elif ord(c)==35:
                        lexActual=lexActual+c
                        estado=9    
                        continue
                    elif ord(c)==39:
                        lexActual=lexActual+c
                        estado=10
                        continue
                    elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                        pass
                    else:
                        error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error)
                    estado=0 
            elif estado==2:
                if self.isSimbolo(c):
                    Tk_Simbolo=Tk_Simbolo+c
                    estado=2
                    contador+=1
                    token=Token(contador,Tk_Simbolo,fila,str(columna - (len(Tk_Simbolo) - 1)),'Simbolo')
                    self.ListaTokens1.append(token)
                    Tk_Simbolo=''
                else:











                    
                    if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                        pass
                    else:
                        error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error)
                    Tk_Simbolo=''
                    estado=0
            elif estado==3:
                if ord(c)!=34:
                    Tk_Cadena=Tk_Cadena+c
                    estado=3
                elif ord(c)==34:
                    contador+=1
                    token=Token(contador,Tk_Cadena,fila,str(columna - (len(Tk_Cadena) - 1)),'Cadena')
                    self.ListaTokens1.append(token)
                    Tk_Cadena=''
                    #
                    Tk_ComillasDobles=Tk_ComillasDobles+c
                    estado=4
                else:
                    if ord(c) == 32 or ord(c) == 9 or ord(c) == 10 or c=='~':
                        pass
                    else:
                        error=Error('Lexico',fila,str(columna - (len(Tk_Cadena) - 1)),'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error)
            elif estado==4:
                contador+=1
                token=Token(contador,Tk_ComillasDobles,fila,columna,'Comillas Dobles')
                self.ListaTokens1.append(token)      
                if ord(c) == 32 or ord(c) == 9 or ord(c) == 10 or c=='~':
                    pass
                else:
                    error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                    self.ListaErrores1.append(error)
                Tk_ComillasDobles=''
                estado=0
                
                
                  


            if (ord(c) == 10):
                columna = 0
                fila += 1
                continue
        #Tab Horizontal
            elif (ord(c) == 9):
                columna += 4
                continue
        #Espacio
            elif (ord(c) == 32):
                columna += 1
                continue
            columna += 1
        
        ##########
        self.ListaTokens=self.ListaTokens1.copy()
        self.ListaErrores=self.ListaErrores1.copy() 
        
        self.ListaTokens1.clear()
        self.ListaErrores1.clear()



    def AccionComboBox(self,event):
        if self.combo.get()=='Generar Reporte de Errores':
            #print('ERRORRRRRR')
            self.Generar_TablaErrores()
        elif self.combo.get()=='Generar Reporte de Tokens':
            self.Generar_TablaTokens()
        elif self.combo.get()=='Generar Árbol de derivación':
            self.Generar_Arbol()


    def Generar_TablaTokens(self):
        for x in self.ListaTokens:
            print(x.Numero,x.lexema,x.fila,x.columna,x.token)
        #
        #
    def Generar_TablaErrores(self):
        for y in self.ListaErrores:
            print(y.tipoError,y.filaError,y.columnaError,y.descripcion,y.caracter)


    def Generar_Arbol(self):
        pass






Aps=Application()
Aps.create_widgets()
Aps.root.mainloop()
