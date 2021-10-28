#from _typeshed import SupportsItemAccess
from os import lseek
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from token import ENCODING, LEFTSHIFTEQUAL
from Error import Error
from Token import Token

class Application():
    def __init__(self):
        self.root = Tk()
        self.root.call('encoding', 'system', 'utf-8')
        self.root.title('SolutionPy')     
        self.root.iconbitmap('Image/Chart.ico')
        self.root.config(bg='#f0f3f4')
        self.root.state('zoomed')
        self.text=''
        self.ListaErrores1=[]
        self.ListaTokens1=[]
        self.ListaErrores=[]
        self.ListaTokens=[]
        self.ListaTokens_T=[]
        self.ListaErrores_T=[]
        self.PalabrasReservadas=['Claves','Registros','imprimir','imprimirln','conteo','promedio','contarsi','datos','sumar','max','min','exportarReporte']
        self.PalabrasReservadasDatos=[]


        self.Claves=[]
        self.Registros1=[]
        self.Registros=[]
        self.Comandos=[]
        self.instruccion=''
        self.campo=''
        self.cadenaimprimir=''
        self.valorcomparar=''
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
        self.TextoEntrada = Text(self.root, height=25, width=89, wrap='none')
        
        scroll = Scrollbar(self.root, command=self.TextoEntrada.yview)
        scrollh=Scrollbar(self.root,orient=HORIZONTAL,command=self.TextoEntrada.xview)
        self.TextoEntrada.configure(yscrollcommand=scroll.set,xscrollcommand=scrollh.set,bg='#fdfefe',foreground='black',font=('Segoe UI', 12,))
        #self.TextoEntrada.place(x=40, y=150,width=820,height=540)
        self.TextoEntrada.place(x=40,y=150)
        #scrollh.config()
        self.TextoEntrada.yview('end')
        ##SCROLL DE CONSOLA
        self.TextConsola=Text (self.root, height=25, width=44, wrap='none')   
        scrollConsola=Scrollbar(self.root,command=self.TextConsola.yview)
        scrollh2=Scrollbar(self.root,command=self.TextConsola.xview,orient=HORIZONTAL)

        self.TextConsola.configure(yscrollcommand=scrollConsola.set,xscrollcommand=scrollh2.set,background='#000000',font=('Segoe UI', 12,),foreground='white',insertbackground='white')
        self.TextConsola.place(x=900, y=150)
        self.TextConsola.yview('end')
        


        scrollConsola.pack(expand=True,padx=10, fill=Y)
        scrollConsola.place(x=1290,y=150,height=540)
        ##
        scroll.pack(expand=True,padx=10, fill=Y)
        scroll.place(x=843,y=150,height=540)

        scrollh.pack(expand=True,padx=10,fill=X)
        scrollh.place(x=40,y=677,width=800)
        scrollh2.pack(expand=True,fill='x')
        scrollh2.place(x=890,y=673,width=400)


        self.combo.bind('<<ComboboxSelected>>', self.AccionComboBox)

    def select_file(self):
      
        filetypes = (('Archivos lfp', '*.lfp'),('Todos los archivos', '*.*'))
        try:
            a=open(filedialog.askopenfilename(title='Abrir un archivo',filetypes=filetypes,initialdir='./'),'r',encoding='utf-8')
            self.text = a.read()
            a.close()
            messagebox.showinfo(title='Información', message='Archivo cargado exitosamente')
            self.TextoEntrada.insert(END,self.text)
        except FileNotFoundError:
            messagebox.showerror(title='Error', message='No se eligió ningún archivo')
            return None

        #archivo = filedialog.askopenfile(title='Abrir un archivo',initialdir='./',filetypes=filetypes)

      



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
        TK_Numeral=''
        Tk_CSimple=''
        Tk_ComentarioMulti=''
        Tk_ComentarioLinea=''
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
                    #columna += 1
                    token=Token(contador,Tk_Simbolo,fila,columna,'Simbolo')
                    self.ListaTokens1.append(token)
                    Tk_Simbolo=''
                elif ord(c)==34:
                    Tk_ComillasDobles=Tk_ComillasDobles+c
                    contador+=1
                    #columna += 1
                    token=Token(contador,Tk_ComillasDobles,fila,columna,'Comillas Dobles')
                    self.ListaTokens1.append(token)
                    Tk_ComillasDobles=''
                    estado=3
                elif ((ord(c)==43) or (ord(c)==45)):
                    Tk_Numero=Tk_Numero+c
                    estado=5
                elif self.isNumero(c):
                    Tk_Numero=Tk_Numero+c
                    estado=6
                elif ord(c)==35:
                    TK_Numeral=TK_Numeral+c
                    estado=9    
                elif ord(c)==39:
                    Tk_CSimple=Tk_CSimple+c
                    estado=10
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
                        columna += 1
                        token=Token(contador,Tk_Simbolo,fila,columna,'Simbolo')
                        self.ListaTokens1.append(token)
                        Tk_Simbolo=''
                        estado=2 #PENDIENTE
                        continue
                    elif self.isLetra(c):
                        Tk_Identificador=Tk_Identificador+c
                        estado=1
                        columna += 1
                        continue
                    elif ord(c)==34:
                        Tk_ComillasDobles=Tk_ComillasDobles+c
                        contador+=1
                        columna += 1
                        token=Token(contador,Tk_ComillasDobles,fila,columna,'Comillas Dobles')
                        self.ListaTokens1.append(token)
                        Tk_ComillasDobles=''
                        estado=3
                        continue
                    elif ((ord(c)==43) or (ord(c)==45)):
                        Tk_Numero=Tk_Numero+c
                        estado=5
                        columna += 1
                        continue
                    elif self.isNumero(c):
                        Tk_Numero=Tk_Numero+c
                        estado=6
                        columna += 1
                        continue
                    elif ord(c)==35:
                        TK_Numeral=TK_Numeral+c
                        estado=9
                        columna += 1    
                        continue
                    elif ord(c)==39:
                        Tk_CSimple=Tk_CSimple+c
                        estado=10
                        columna += 1
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
                    #contador+=1
                    #columna += 1
                    token=Token(contador,Tk_Simbolo,fila,columna,'Simbolo')
                    self.ListaTokens1.append(token)
                    Tk_Simbolo=''
                else:
                    if self.isSimbolo(c):
                        Tk_Simbolo=Tk_Simbolo+c
                        contador+=1
                        columna += 1
                        token=Token(contador,Tk_Simbolo,fila,columna,'Simbolo')
                        self.ListaTokens1.append(token)
                        Tk_Simbolo=''
                        estado=0 #PENDIENTE
                        continue
                    elif self.isLetra(c):
                        Tk_Identificador=Tk_Identificador+c
                        columna += 1
                        estado=1
                        continue
                    elif ord(c)==34:
                        Tk_ComillasDobles=Tk_ComillasDobles+c
                        contador+=1
                        columna += 1
                        token=Token(contador,Tk_ComillasDobles,fila,columna,'Comillas Dobles')
                        self.ListaTokens1.append(token)
                        Tk_ComillasDobles=''
                        estado=3
                        continue
                    elif ((ord(c)==43) or (ord(c)==45)):
                        Tk_Numero=Tk_Numero+c
                        columna += 1
                        estado=5
                        continue
                    elif self.isNumero(c):
                        Tk_Numero=Tk_Numero+c
                        columna += 1
                        estado=6
                        continue
                    elif ord(c)==35:
                        TK_Numeral=TK_Numeral+c
                        columna += 1
                        estado=9    
                        continue
                    elif ord(c)==39:
                        Tk_CSimple=Tk_CSimple+c
                        columna += 1
                        estado=10
                        continue
                    elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                        pass
                    else:
                        error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error)
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
                        error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error)
            elif estado==4:
                contador+=1
                token=Token(contador,Tk_ComillasDobles,fila,columna,'Comillas Dobles')
                self.ListaTokens1.append(token)
                Tk_ComillasDobles=''
                if self.isSimbolo(c):
                    Tk_Simbolo=Tk_Simbolo+c
                    contador+=1
                    columna += 1
                    token=Token(contador,Tk_Simbolo,fila,columna,'Simbolo')
                    self.ListaTokens1.append(token)
                    Tk_Simbolo=''
                    estado=0 #PENDIENTE
                    continue
                elif self.isLetra(c):
                    Tk_Identificador=Tk_Identificador+c
                    estado=1
                    columna += 1
                    continue
                elif ord(c)==34:
                    Tk_ComillasDobles=Tk_ComillasDobles+c
                    contador+=1
                    columna += 1
                    token=Token(contador,Tk_ComillasDobles,fila,columna,'Comillas Dobles')
                    self.ListaTokens1.append(token)
                    Tk_ComillasDobles=''
                    estado=3
                    continue
                elif ((ord(c)==43) or (ord(c)==45)):
                    Tk_Numero=Tk_Numero+c
                    estado=5
                    columna += 1
                    continue
                elif self.isNumero(c):
                    Tk_Numero=Tk_Numero+c
                    estado=6
                    columna += 1
                    continue
                elif ord(c)==35:
                    TK_Numeral=TK_Numeral+c
                    estado=9   
                    columna += 1 
                    continue
                elif ord(c)==39:
                    Tk_CSimple=Tk_CSimple+c
                    estado=10
                    columna += 1
                    continue
                elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                    pass
                else:
                    error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                    self.ListaErrores1.append(error)      
                estado=0
            elif estado==5:
                if self.isNumero(c):
                    Tk_Numero=Tk_Numero+c
                    estado=6
                else:
                    if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                        pass
                    else:
                        error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error)
            elif estado==6:
                if self.isNumero(c):
                    Tk_Numero=Tk_Numero+c
                    estado=6
                elif ord(c)==46:
                    Tk_Numero=Tk_Numero+c
                    estado=7
                else:
                    contador+=1
                    token=Token(contador,Tk_Numero,fila,columna,'Numero')
                    self.ListaTokens1.append(token)
                    Tk_Numero=''
                    if self.isSimbolo(c):
                        Tk_Simbolo=Tk_Simbolo+c
                        contador+=1
                        columna += 1
                        token=Token(contador,Tk_Simbolo,fila,columna,'Simbolo')
                        self.ListaTokens1.append(token)
                        Tk_Simbolo=''
                        estado=0 #PENDIENTE
                        continue
                    elif self.isLetra(c):
                        Tk_Identificador=Tk_Identificador+c
                        estado=1
                        columna += 1
                        continue
                    elif ord(c)==34:
                        Tk_ComillasDobles=Tk_ComillasDobles+c
                        contador+=1
                        columna += 1
                        token=Token(contador,Tk_ComillasDobles,fila,columna,'Comillas Dobles')
                        self.ListaTokens1.append(token)
                        Tk_ComillasDobles=''
                        estado=3
                        continue
                    elif ((ord(c)==43) or (ord(c)==45)):
                        Tk_Numero=Tk_Numero+c
                        estado=5
                        columna += 1
                        continue
                    elif self.isNumero(c):
                        Tk_Numero=Tk_Numero+c
                        estado=6
                        columna += 1
                        continue
                    elif ord(c)==35:
                        TK_Numeral=TK_Numeral+c
                        estado=9   
                        columna += 1 
                        continue
                    elif ord(c)==39:
                        Tk_CSimple=Tk_CSimple+c
                        estado=10
                        columna += 1
                        continue
                    elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                        pass
                    else:
                        error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error)      
                    estado=0
                    
            elif estado==7:
                if self.isNumero(c):
                    Tk_Numero=Tk_Numero+c
                    estado=8
                else:
                    if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                        pass
                    else:
                        error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error)    
            elif estado==8:
                if self.isNumero(c):
                    Tk_Numero=Tk_Numero+c
                    estado=8
                else:
                    contador+=1
                    token=Token(contador,Tk_Numero,fila,columna,'Numero')
                    self.ListaTokens1.append(token)
                    Tk_Numero=''
                    if self.isSimbolo(c):
                        Tk_Simbolo=Tk_Simbolo+c
                        contador+=1
                        columna += 1
                        token=Token(contador,Tk_Simbolo,fila,columna,'Simbolo')
                        self.ListaTokens1.append(token)
                        Tk_Simbolo=''
                        estado=0 #PENDIENTE
                        continue
                    elif self.isLetra(c):
                        Tk_Identificador=Tk_Identificador+c
                        estado=1
                        columna += 1
                        continue
                    elif ord(c)==34:
                        Tk_ComillasDobles=Tk_ComillasDobles+c
                        contador+=1
                        columna += 1
                        token=Token(contador,Tk_ComillasDobles,fila,columna,'Comillas Dobles')
                        self.ListaTokens1.append(token)
                        Tk_ComillasDobles=''
                        estado=3
                        continue
                    elif ((ord(c)==43) or (ord(c)==45)):
                        Tk_Numero=Tk_Numero+c
                        estado=5
                        columna += 1
                        continue
                    elif self.isNumero(c):
                        Tk_Numero=Tk_Numero+c
                        estado=6
                        columna += 1
                        continue
                    elif ord(c)==35:
                        TK_Numeral=TK_Numeral+c
                        estado=9    
                        columna += 1
                        continue
                    elif ord(c)==39:
                        Tk_CSimple=Tk_CSimple+c
                        estado=10
                        columna += 1
                        continue
                    elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                        pass
                    else:
                        error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error)      
                    estado=0
            elif estado==9:
                if ord(c)!=10:
                    Tk_ComentarioLinea=Tk_ComentarioLinea+c
                else:
                    Tk_ComentarioLinea=''
                    if self.isSimbolo(c):
                        Tk_Simbolo=Tk_Simbolo+c
                        contador+=1
                        columna += 1
                        token=Token(contador,Tk_Simbolo,fila,columna,'Simbolo')
                        self.ListaTokens1.append(token)
                        Tk_Simbolo=''
                        estado=0 #PENDIENTE
                        continue
                    elif self.isLetra(c):
                        Tk_Identificador=Tk_Identificador+c
                        estado=1
                        columna += 1
                        continue
                    elif ord(c)==34:
                        Tk_ComillasDobles=Tk_ComillasDobles+c
                        contador+=1
                        columna += 1
                        token=Token(contador,Tk_ComillasDobles,fila,columna,'Comillas Dobles')
                        self.ListaTokens1.append(token)
                        Tk_ComillasDobles=''
                        estado=3
                        continue
                    elif ((ord(c)==43) or (ord(c)==45)):
                        Tk_Numero=Tk_Numero+c
                        estado=5
                        columna += 1
                        continue
                    elif self.isNumero(c):
                        Tk_Numero=Tk_Numero+c
                        estado=6
                        columna += 1
                        continue
                    elif ord(c)==35:
                        TK_Numeral=TK_Numeral+c
                        estado=9    
                        columna += 1
                        continue
                    elif ord(c)==39:
                        Tk_CSimple=Tk_CSimple+c
                        estado=10
                        columna += 1
                        continue
                    elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                        pass
                    else:
                        error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error)      
                    estado=0
            elif estado==10:
                if ord(c)==39:
                    Tk_CSimple=Tk_CSimple+c
                    estado=11
                else:
                    if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                        pass
                    else:
                        error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error)   
            elif estado==11:
                if ord(c)==39:
                    Tk_CSimple=Tk_CSimple+c
                    #aqui agregaria el token comilla simple
                    Tk_CSimple=''
                    estado=12
                else:
                    if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                        pass
                    else:
                        error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error) 
            elif estado==12:
                if ord(c)!=39:
                    Tk_ComentarioMulti=Tk_ComentarioMulti+c
                    estado=12
                elif ord(c)==39:
                    #aqui agregaria el token comentario
                    Tk_ComentarioMulti=''
                    Tk_CSimple=Tk_CSimple+c
                    estado=13
                else:
                    if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                        pass
                    else:
                        error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error)      
            elif estado==13:
                if ord(c)==39:
                    Tk_CSimple=Tk_CSimple+c
                    estado=14
                else:
                    if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                        pass
                    else:
                        error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error)
            elif estado==14:
                if ord(c)==39:
                    Tk_CSimple=Tk_CSimple+c
                    estado=15
                else:
                    if ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                        pass
                    else:
                        error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                        self.ListaErrores1.append(error)
            elif estado==15:
                Tk_CSimple=''
                if self.isSimbolo(c):
                    Tk_Simbolo=Tk_Simbolo+c
                    contador+=1
                    columna += 1
                    token=Token(contador,Tk_Simbolo,fila,columna,'Simbolo')
                    self.ListaTokens1.append(token)
                    Tk_Simbolo=''
                    estado=0 #PENDIENTE
                    continue
                elif self.isLetra(c):
                    Tk_Identificador=Tk_Identificador+c
                    estado=1
                    columna += 1
                    continue
                elif ord(c)==34:
                    Tk_ComillasDobles=Tk_ComillasDobles+c
                    contador+=1
                    columna += 1
                    token=Token(contador,Tk_ComillasDobles,fila,columna,'Comillas Dobles')
                    self.ListaTokens1.append(token)
                    Tk_ComillasDobles=''
                    estado=3
                    continue
                elif ((ord(c)==43) or (ord(c)==45)):
                    Tk_Numero=Tk_Numero+c
                    estado=5
                    columna += 1
                    continue
                elif self.isNumero(c):
                    Tk_Numero=Tk_Numero+c
                    estado=6
                    columna += 1
                    continue
                elif ord(c)==35:
                    TK_Numeral=TK_Numeral+c
                    estado=9    
                    columna += 1
                    continue
                elif ord(c)==39:
                    Tk_CSimple=Tk_CSimple+c
                    estado=10
                    columna += 1
                    continue
                elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9 or c=='~':
                    pass
                else:
                    error=Error('Lexico',fila,columna,'Se detecto un caracter invalido',c)
                    self.ListaErrores1.append(error)      
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
        acept=Token(contador+1,'~',None,None,'Aceptacion')
        self.ListaTokens1.append(acept)
        self.ListaTokens=self.ListaTokens1.copy()
        
        #self.ListaErrores=self.ListaErrores1.copy()
        ########
        self.ListaTokens_T=self.ListaTokens1.copy()
        #self.ListaErrores_T=self.ListaErrores1.copy()
        self.ListaTokens1.clear()

        self.estado_inicial()

     



     
    def estado_inicial(self):
        self.TextConsola.config(state='normal')

        #for l in self.ListaTokens:
        #    print(l.lexema,l.token)
        self.p_CLaves1()
        
    def p_CLaves1(self):
        if self.ListaTokens[0].token=='Palabra Reservada' and self.ListaTokens[0].lexema=='Claves':
            self.ListaTokens.pop(0)
            self.p_Claves2()
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba Claves',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error)
            self.ListaTokens.pop(0)
            self.p_Claves2()

    def p_Claves2(self):
        if self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema=='=':
            self.ListaTokens.pop(0)
            self.p_Claves3()
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba =',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error)
            self.ListaTokens.pop(0)
            self.p_Claves3()

    def p_Claves3(self):
        if self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema=='[':
            self.ListaTokens.pop(0)
            self.ver_ListaClaves()
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba [',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error)
            self.ListaTokens.pop(0)
            self.ver_ListaClaves()

    def ver_ListaClaves(self):
        self.ver_elemento()

    def ver_elemento(self):
        if self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"':
            self.ListaTokens.pop(0)
            if self.ListaTokens[0].token=='Cadena':
                self.Claves.append(self.ListaTokens[0].lexema)
                self.ListaTokens.pop(0)
                if self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"':
                    self.ListaTokens.pop(0)
                    self.ver_ListaClaves_p()
                else:
                    error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba "',self.ListaTokens[0].lexema)
                    self.ListaErrores1.append(error)
                    self.ListaTokens.pop(0)
                    self.ver_ListaClaves_p()
            else:
                error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba una Cadena',self.ListaTokens[0].lexema)
                self.ListaErrores1.append(error)
                self.ListaTokens.pop(0)
                self.ver_ListaClaves_p()
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba "',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error)
            self.ListaTokens.pop(0)
            self.ver_ListaClaves_p()
            



    def ver_ListaClaves_p(self):
        if self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==',':
            self.ListaTokens.pop(0)
            self.ver_ListaClaves()
        elif self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==']':
            self.ListaTokens.pop(0)
            self.ver_Registros()
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba , o ]',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error)
            self.ListaTokens.pop(0)
            self.ver_Registros()


            ##########################################

    def ver_Registros(self):
        if self.ListaTokens[0].token=='Palabra Reservada' and self.ListaTokens[0].lexema=='Registros':
            self.ListaTokens.pop(0)
            self.ver_Registros2()
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba Registros',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error)
            self.ListaTokens.pop(0)
            self.ver_Registros2()

    def ver_Registros2(self):
        if self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema=='=':
            self.ListaTokens.pop(0)
            self.ver_Registros3()
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba =',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error)
            self.ListaTokens.pop(0)
            self.ver_Registros3()

    def ver_Registros3(self):
        if self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema=='[':
            self.ListaTokens.pop(0)
            self.ver_ListaRegistros()
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba [',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error)
            self.ListaTokens.pop(0)
            self.ver_ListaRegistros()



    def ver_ListaRegistros(self):
        self.ver_Registro()

    def ver_Registro(self):
        if self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema=='{':
            self.ListaTokens.pop(0)
            self.Ver_ListaElementoRegistro()
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba {',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error)
            self.ListaTokens.pop(0)
            self.Ver_ListaElementoRegistro()




    def Ver_ListaElementoRegistro(self):
        self.Ver_ElementoRegistro()
    
    def Ver_ElementoRegistro(self):
        if self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"':
            self.ListaTokens.pop(0)
            if self.ListaTokens[0].token=='Cadena':
                self.Registros1.append(self.ListaTokens[0].lexema)
                self.ListaTokens.pop(0)
                if self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"':
                    self.ListaTokens.pop(0)
                    self.ver_ListaElementoRegistro_p()
                else:
                    error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba "',self.ListaTokens[0].lexema)
                    self.ListaErrores1.append(error)
                    self.ListaTokens.pop(0)
                    self.ver_ListaElementoRegistro_p()


            else:
                error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba una Cadena',self.ListaTokens[0].lexema)
                self.ListaErrores1.append(error)
                self.ListaTokens.pop(0)
                self.ver_ListaElementoRegistro_p()
        else:
            if self.ListaTokens[0].token=='Numero':
                if self.ListaTokens[0].lexema.isdigit():
                    self.Registros1.append(int(self.ListaTokens[0].lexema))
                else:
                    self.Registros1.append(float(self.ListaTokens[0].lexema))

                self.ListaTokens.pop(0)    
                self.ver_ListaElementoRegistro_p()
            else:
                error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba numero o Comillas Dobles',self.ListaTokens[0].lexema)
                self.ListaErrores1.append(error)
                self.ListaTokens.pop(0)
                self.ver_ListaElementoRegistro_p()

       


    def ver_ListaElementoRegistro_p(self):
        if self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==',':
            self.ListaTokens.pop(0)
            self.Ver_ListaElementoRegistro()
        elif self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema=='}':
            s=self.Registros1.copy()
            self.Registros.append(s)
            self.Registros1.clear()
            self.ListaTokens.pop(0)
            self.Ver_ListaRegistro_P()
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba , o }',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error)
            self.ListaTokens.pop(0)
            self.Ver_ListaRegistro_P()

    def Ver_ListaRegistro_P(self):
        if self.ListaTokens[0].lexema=='{' and self.ListaTokens[0].token=='Simbolo':
            self.ListaTokens.pop(0)
            self.Ver_ListaElementoRegistro()
        elif self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==']':
            self.ListaTokens.pop(0)
            self.ver_Reportes()
            #print(self.Registros)
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba { o ]',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error) 
            self.ListaTokens.pop(0)
            self.ver_Reportes()
    ############################################
    def ver_Reportes(self):
        #print(self.ListaTokens[-1].lexema, self.ListaTokens[-1].token)
        if self.ListaTokens[0].token=='Palabra Reservada' and self.ListaTokens[0].lexema=='imprimir':
            self.instruccion=self.ListaTokens[0].lexema
            self.ListaTokens.pop(0)
            self.ver_Reportes2()
        elif self.ListaTokens[0].token=='Palabra Reservada' and self.ListaTokens[0].lexema=='imprimirln':
            self.instruccion=self.ListaTokens[0].lexema
            self.ListaTokens.pop(0)
            self.ver_Reportes2()
        elif self.ListaTokens[0].token=='Palabra Reservada' and self.ListaTokens[0].lexema=='exportarReporte':
            self.instruccion=self.ListaTokens[0].lexema
            self.ListaTokens.pop(0)
            self.ver_Reportes2()
        elif self.ListaTokens[0].token=='Palabra Reservada' and self.ListaTokens[0].lexema=='conteo':
            self.instruccion=self.ListaTokens[0].lexema
            self.ListaTokens.pop(0)
            self.ver_Reportes2()
        elif self.ListaTokens[0].token=='Palabra Reservada' and self.ListaTokens[0].lexema=='datos':
            self.instruccion=self.ListaTokens[0].lexema
            self.ListaTokens.pop(0)
            self.ver_Reportes2()
        elif self.ListaTokens[0].token=='Palabra Reservada' and self.ListaTokens[0].lexema=='promedio':
            self.instruccion=self.ListaTokens[0].lexema
            self.ListaTokens.pop(0)
            self.ver_Reportes2()     
        elif self.ListaTokens[0].token=='Palabra Reservada' and self.ListaTokens[0].lexema=='max':
            self.instruccion=self.ListaTokens[0].lexema
            self.ListaTokens.pop(0)
            self.ver_Reportes2()
        elif self.ListaTokens[0].token=='Palabra Reservada' and self.ListaTokens[0].lexema=='sumar':
            self.instruccion=self.ListaTokens[0].lexema
            self.ListaTokens.pop(0)
            self.ver_Reportes2()
        elif self.ListaTokens[0].token=='Palabra Reservada' and self.ListaTokens[0].lexema=='min':
            self.instruccion=self.ListaTokens[0].lexema
            self.ListaTokens.pop(0)
            self.ver_Reportes2()
        elif self.ListaTokens[0].token=='Palabra Reservada' and self.ListaTokens[0].lexema=='contarsi':
            self.instruccion=self.ListaTokens[0].lexema
            self.ListaTokens.pop(0)
            self.ver_Reportes2()   
        elif self.ListaTokens[0].lexema=='~' and self.ListaTokens[0].token=='Aceptacion':
            for l in self.ListaErrores1:
                print(l.caracter,l.descripcion)
            #self.ListaErrores1.clear()
            self.ListaErrores=self.ListaErrores1.copy()
            self.ListaErrores1.clear()
            self.acciones()

            self.Claves.clear()
            self.Comandos.clear()
            self.Registros.clear()
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba una instrucción',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error)
            self.ListaTokens.pop(0)
            self.ver_Reportes2() 

    def ver_Reportes2(self):
        print(self.instruccion)
        if self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema=='(':
            self.ListaTokens.pop(0)
            self.verCampo()
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba (',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error) 
            self.ListaTokens.pop(0)
            self.verCampo()
        
    def verCampo(self):
        if self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='imprimir':
            self.ListaTokens.pop(0)
            if self.ListaTokens[0].token=='Cadena' and self.instruccion=='imprimir':
                self.cadenaimprimir=self.ListaTokens[0].lexema
                self.ListaTokens.pop(0)
                if self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='imprimir':
                    self.ListaTokens.pop(0)
                    self.ver_Reportes3()
                else:
                    error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba "',self.ListaTokens[0].lexema)
                    self.ListaErrores1.append(error)
                    self.ListaTokens.pop(0)
                    self.ver_Reportes3()

            else:
                error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba una Cadena',self.ListaTokens[0].lexema)
                self.ListaErrores1.append(error)
                self.ListaTokens.pop(0)
                self.ver_Reportes3()

        elif self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='imprimirln':
            self.ListaTokens.pop(0)
            if self.ListaTokens[0].token=='Cadena' and self.instruccion=='imprimirln':
                self.cadenaimprimir=self.ListaTokens[0].lexema
                self.ListaTokens.pop(0)
                if self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='imprimirln':
                    self.ListaTokens.pop(0)
                    self.ver_Reportes3()
                else:
                    error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba "',self.ListaTokens[0].lexema)
                    self.ListaErrores1.append(error) 
                    self.ListaTokens.pop(0)
                    self.ver_Reportes3()
            else:
                error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba Cadena',self.ListaTokens[0].lexema)
                self.ListaErrores1.append(error)
                self.ListaTokens.pop(0)
                self.ver_Reportes3()



        elif self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='exportarReporte':
            self.ListaTokens.pop(0)
            if self.ListaTokens[0].token=='Cadena' and self.instruccion=='exportarReporte':
                self.cadenaimprimir=self.ListaTokens[0].lexema
                self.ListaTokens.pop(0)
                if self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='exportarReporte':
                    self.ListaTokens.pop(0)
                    self.ver_Reportes3()
                else:
                    error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba "',self.ListaTokens[0].lexema)
                    self.ListaErrores1.append(error) 
                    self.ListaTokens.pop(0)
                    self.ver_Reportes3()
            else:
                error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba Cadena',self.ListaTokens[0].lexema)
                self.ListaErrores1.append(error)
                self.ListaTokens.pop(0)
                self.ver_Reportes3()



        elif self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==')' and self.instruccion=='conteo':
            self.ListaTokens.pop(0)
            self.ver_Reportes4()
        elif self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==')' and self.instruccion=='datos':
            self.ListaTokens.pop(0)
            self.ver_Reportes4()
        elif self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='promedio':
            self.ListaTokens.pop(0)
            if self.ListaTokens[0].token=='Cadena' and self.instruccion=='promedio' and self.isClave(self.ListaTokens[0].lexema):
                self.campo=self.ListaTokens[0].lexema
                self.ListaTokens.pop(0)
                if self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='promedio':
                    self.ListaTokens.pop(0)
                    self.ver_Reportes3()
                else:
                    error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba "',self.ListaTokens[0].lexema)
                    self.ListaErrores1.append(error) 
                    self.ListaTokens.pop(0)
                    self.ver_Reportes3()
            else:
                error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba Cadena y Campo Válido',self.ListaTokens[0].lexema)
                self.ListaErrores1.append(error)
                self.ListaTokens.pop(0)
                self.ver_Reportes3()



        elif self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='max':
            self.ListaTokens.pop(0)
            if self.ListaTokens[0].token=='Cadena' and self.instruccion=='max' and self.isClave(self.ListaTokens[0].lexema):
                self.campo=self.ListaTokens[0].lexema
                self.ListaTokens.pop(0)
                if self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='max':
                    self.ListaTokens.pop(0)
                    self.ver_Reportes3()
                else:
                    error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba "',self.ListaTokens[0].lexema)
                    self.ListaErrores1.append(error) 
                    self.ListaTokens.pop(0)
                    self.ver_Reportes3()
            else:
                error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba Cadena y Campo Válido',self.ListaTokens[0].lexema)
                self.ListaErrores1.append(error)
                self.ListaTokens.pop(0)
                self.ver_Reportes3()


        elif self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='min':
            self.ListaTokens.pop(0)
            if self.ListaTokens[0].token=='Cadena' and self.instruccion=='min' and self.isClave(self.ListaTokens[0].lexema):
                self.campo=self.ListaTokens[0].lexema
                self.ListaTokens.pop(0)
                if self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='min':
                    self.ListaTokens.pop(0)
                    self.ver_Reportes3()
                else:
                    error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba "',self.ListaTokens[0].lexema)
                    self.ListaErrores1.append(error) 
                    self.ListaTokens.pop(0)
                    self.ver_Reportes3()
            else:
                error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba Cadena y Campo Válido',self.ListaTokens[0].lexema)
                self.ListaErrores1.append(error)
                self.ListaTokens.pop(0)
                self.ver_Reportes3()



        elif self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='sumar':
            self.ListaTokens.pop(0)
            if self.ListaTokens[0].token=='Cadena' and self.instruccion=='sumar' and self.isClave(self.ListaTokens[0].lexema):
                self.campo=self.ListaTokens[0].lexema
                self.ListaTokens.pop(0)
                if self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='sumar':
                    self.ListaTokens.pop(0)
                    self.ver_Reportes3()
                else:
                    error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba "',self.ListaTokens[0].lexema)
                    self.ListaErrores1.append(error) 
                    self.ListaTokens.pop(0)
                    self.ver_Reportes3()
            else:
                error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba Cadena y Campo Válido',self.ListaTokens[0].lexema)
                self.ListaErrores1.append(error)
                self.ListaTokens.pop(0)
                self.ver_Reportes3()
            
        elif self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='contarsi':
            self.ListaTokens.pop(0)
            if self.ListaTokens[0].token=='Cadena' and self.instruccion=='contarsi' and self.isClave(self.ListaTokens[0].lexema):
                self.campo=self.ListaTokens[0].lexema
                self.ListaTokens.pop(0)
                if self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='contarsi':
                    self.ListaTokens.pop(0)
                    if self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==',' and self.instruccion=='contarsi':
                        self.ListaTokens.pop(0)                        
                        if self.ListaTokens[0].token=='Numero':
                            self.valorcomparar=self.ListaTokens[0].lexema
                            self.ListaTokens.pop(0)
                            self.ver_Reportes3()
                        elif self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='contarsi':
                            self.ListaTokens.pop(0)
                            if self.ListaTokens[0].token=='Cadena' and self.instruccion=='contarsi':
                                self.valorcomparar=self.ListaTokens[0].lexema
                                self.ListaTokens.pop(0)
                                if self.ListaTokens[0].token=='Comillas Dobles' and self.ListaTokens[0].lexema=='"' and self.instruccion=='contarsi':
                                    self.ListaTokens.pop(0)
                                    self.ver_Reportes3()
                                else:
                                    error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba "',self.ListaTokens[0].lexema)
                                    self.ListaErrores1.append(error) 
                                    self.ListaTokens.pop(0)
                                    self.ver_Reportes3()
                            else:
                                error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba cadena',self.ListaTokens[0].lexema)
                                self.ListaErrores1.append(error)
                                self.ListaTokens.pop(0)
                                self.ver_Reportes3()
                        else:
                            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba una cadena o numero',self.ListaTokens[0].lexema)
                            self.ListaErrores1.append(error) 
                            self.ListaTokens.pop(0)
                            self.ver_Reportes3()
                    else:
                        error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba ,',self.ListaTokens[0].lexema)
                        self.ListaErrores1.append(error) 
                        self.ListaTokens.pop(0)
                        self.ver_Reportes3()
                else:
                    error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba "',self.ListaTokens[0].lexema)
                    self.ListaErrores1.append(error) 
                    self.ListaTokens.pop(0)
                    self.ver_Reportes3()
            else:
                error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba Cadena y Campo Válido',self.ListaTokens[0].lexema)
                self.ListaErrores1.append(error)
                self.ListaTokens.pop(0)
                self.ver_Reportes3()
        
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba Cadena',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error)
            self.ListaTokens.pop(0)
            self.ver_Reportes3()
    def ver_Reportes3(self):
        if self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==')':
            self.ListaTokens.pop(0)
            self.ver_Reportes4()
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba )',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error)
            self.ListaTokens.pop(0)
            self.ver_Reportes4()

    def ver_Reportes4(self):
        if self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==';' and self.instruccion=='imprimir':
            listatemporal=[self.instruccion,self.cadenaimprimir]
            ls=listatemporal.copy()
            self.Comandos.append(ls)
            listatemporal.clear()
            self.ListaTokens.pop(0)
            self.instruccion=''
            self.cadenaimprimir=''
            self.ver_Reportes()
        elif self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==';' and self.instruccion=='imprimirln':
            listatemporal=[self.instruccion,self.cadenaimprimir]
            ls=listatemporal.copy()
            self.Comandos.append(ls)
            listatemporal.clear()
            self.ListaTokens.pop(0)
            self.instruccion=''
            self.cadenaimprimir=''
            self.ver_Reportes()
        elif self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==';' and self.instruccion=='exportarReporte':
            listatemporal=[self.instruccion,self.cadenaimprimir]
            ls=listatemporal.copy()
            self.Comandos.append(ls)
            listatemporal.clear()
            self.ListaTokens.pop(0)
            self.instruccion=''
            self.cadenaimprimir=''
            self.ver_Reportes()
        elif self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==';' and self.instruccion=='conteo':
            listatemporal1=[self.instruccion]
            ls1=listatemporal1.copy()
            self.Comandos.append(ls1)
            listatemporal1.clear()
            self.ListaTokens.pop(0)
            self.instruccion=''
            self.ver_Reportes()
        elif self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==';' and self.instruccion=='datos':
            listatemporal1=[self.instruccion]
            ls1=listatemporal1.copy()
            self.Comandos.append(ls1)
            listatemporal1.clear()
            self.ListaTokens.pop(0)
            self.instruccion=''
            self.ver_Reportes()
        elif self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==';' and self.instruccion=='promedio':
            listatemporal2=[self.instruccion,self.campo]
            ls2=listatemporal2.copy()
            self.Comandos.append(ls2)
            listatemporal2.clear()
            self.ListaTokens.pop(0)
            self.instruccion=''
            self.campo=''
            self.ver_Reportes()
        elif self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==';' and self.instruccion=='max':
            listatemporal2=[self.instruccion,self.campo]
            ls2=listatemporal2.copy()
            self.Comandos.append(ls2)
            listatemporal2.clear()
            self.ListaTokens.pop(0)
            self.instruccion=''
            self.campo=''
            self.ver_Reportes()
        elif self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==';' and self.instruccion=='min':
            listatemporal2=[self.instruccion,self.campo]
            ls2=listatemporal2.copy()
            self.Comandos.append(ls2)
            listatemporal2.clear()
            self.ListaTokens.pop(0)
            self.instruccion=''
            self.campo=''
            self.ver_Reportes()
        elif self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==';' and self.instruccion=='sumar':
            listatemporal2=[self.instruccion,self.campo]
            ls2=listatemporal2.copy()
            self.Comandos.append(ls2)
            listatemporal2.clear()
            self.ListaTokens.pop(0)
            self.instruccion=''
            self.campo=''
            self.ver_Reportes()
        elif self.ListaTokens[0].token=='Simbolo' and self.ListaTokens[0].lexema==';' and self.instruccion=='contarsi':
            listatemporal3=[self.instruccion,self.campo,self.valorcomparar]
            ls3=listatemporal3.copy()
            self.Comandos.append(ls3)
            listatemporal3.clear()
            self.ListaTokens.pop(0)
            self.instruccion=''
            self.campo=''
            self.valorcomparar=''
            self.ver_Reportes()

        
        else:
            error=Error('Sintactico',self.ListaTokens[0].fila,self.ListaTokens[0].columna,'Se esperaba ;',self.ListaTokens[0].lexema)
            self.ListaErrores1.append(error) 
            self.ver_Reportes()

            
        
    
        
    def isClave(self,texto):
        for i in self.Claves:
            if i==texto:
                return True
        return False
            


    def acciones(self):
        
        textoim=''
        textosalto=''
        if self.Comandos is None:
            self.TextConsola.insert(INSERT,'No hay comandos para ejecutar D:')
        else:
            for s in range(len(self.Comandos)):
                if self.Comandos[s][0]=='imprimir':
                    self.TextConsola.insert(END,self.Comandos[s][1])             
                elif self.Comandos[s][0]=='imprimirln':
                    self.TextConsola.insert(END,self.Comandos[s][1]+'\n')
                elif self.Comandos[s][0]=='exportarReporte':
                    self.tabla_registros(self.Comandos[s][1]) 
                    self.TextConsola.insert(END,'> Tabla generada')
                elif self.Comandos[s][0]=='conteo':
                    self.TextConsola.insert(END,f'> {len(self.Registros)}')
                elif self.Comandos[s][0]=='datos':
                    texto1=''
                    for l in self.Claves:
                        self.TextConsola.insert(END,f'    {l}')

                    self.TextConsola.insert(END,'\n')
                    for j in range(len(self.Registros)):
                        for k in range(len(self.Registros[j])):
                            self.TextConsola.insert(END,f'    {self.Registros[j][k]} |')
                        self.TextConsola.insert(END,'\n')
                    
                elif self.Comandos[s][0]=='promedio':
                    self.TextConsola.insert(END,'> '+str(self.promedio(self.Comandos[s][1])))
                elif self.Comandos[s][0]=='max':
                    self.TextConsola.insert(END,'> '+str(self.max(self.Comandos[s][1])))
                elif self.Comandos[s][0]=='min':
                    self.TextConsola.insert(END,'> '+str(self.min(self.Comandos[s][1])))
                elif self.Comandos[s][0]=='sumar':
                    self.TextConsola.insert(END,'> '+str(self.sumar(self.Comandos[s][1])))
                elif self.Comandos[s][0]=='contarsi':

                    print(self.Comandos)
                    self.TextConsola.insert(END,'> '+str(self.contarsi(self.Comandos[s][1],self.Comandos[s][2])))  

        #self.TextConsola.configure(state='disabled')
        
        self.TextConsola.config(state='disabled')
        self.TextConsola.see('end')
        


    def contarsi(self,campo,valorcomparar):
        ent=None
        flo=None
        st=None
        listaIguales=[]
        try:
            int(valorcomparar)
            ent = True
            flo=False
            st=False
        except ValueError:
            try:
                float(valorcomparar)
                flo = True
                ent=False
                st=False
            except ValueError:
                st=True
                flo=False
                ent=False
        
        if ent:
            for a in range(len(self.Claves)):
                if self.Claves[a]==campo:
                    for j in range(len(self.Registros)):
                        if self.Registros[j][a]==int(valorcomparar):
                            listaIguales.append(self.Registros[j][a])
        elif flo:
            for a in range(len(self.Claves)):
                if self.Claves[a]==campo:
                    for j in range(len(self.Registros)):
                        if self.Registros[j][a]==float(valorcomparar):
                            listaIguales.append(self.Registros[j][a])
        elif st:
            for a in range(len(self.Claves)):
                if self.Claves[a]==campo:
                    for j in range(len(self.Registros)):
                        if self.Registros[j][a]==str(valorcomparar):
                            listaIguales.append(self.Registros[j][a])

        return len(listaIguales)




      



    def sumar(self,campo):
        listaSuma=[]
        for a in range(len(self.Claves)):
            if self.Claves[a]==campo:
                for j in range(len(self.Registros)):
                    listaSuma.append(self.Registros[j][a])
        suma=0
        for k in listaSuma:
            suma+=k

        return suma

    def min(self,campo):
        listaMin=[]
        for a in range(len(self.Claves)):
            if self.Claves[a]==campo:
                for j in range(len(self.Registros)):
                    listaMin.append(self.Registros[j][a])
        notamin=min(listaMin)
        return notamin

    def max(self,campo):
        listaMax=[]
        for a in range(len(self.Claves)):
            if self.Claves[a]==campo:
                for j in range(len(self.Registros)):
                    listaMax.append(self.Registros[j][a])

        notamax=max(listaMax)

        return notamax


    def promedio(self,campo):
        suma=0
        for a in range(len(self.Claves)):
            if self.Claves[a]==campo:
                for j in range(len(self.Registros)):
                    suma=suma+self.Registros[j][a]
        
        pr=suma/len(self.Registros)
        return pr

    def v_datos(self):
        texto=''
        for l in self.Claves:
            texto+=f"""    {l}   |   """
        texto+='\n'
        for j in range(len(self.Registros)):

            for k in range(len(self.Registros[j])):
                texto+=f"""    {self.Registros[j][k]}   |   """
            texto+='\n'
                
        return texto


    def p_Registros(self):
        pass
    def A_prima(self):
        pass




    def AccionComboBox(self,event):
        if self.combo.get()=='Generar Reporte de Errores':
            print(self.ListaErrores)
            self.Generar_TablaErrores()
        elif self.combo.get()=='Generar Reporte de Tokens':
            self.Generar_TablaTokens()
        elif self.combo.get()=='Generar Árbol de derivación':
            self.Generar_Arbol()
    def tabla_registros(self,titulo):
        Rhtml=open(f'Registros/index.html','w')
        txRegistro=''
        txRegistro+="""
        <!DOCTYPE html> 
        <html lang="en">
        <head>
	    <title>Registros | LFP</title>
	    <meta charset="UTF-8">
	    <meta name="viewport" content="width=device-width, initial-scale=1">
        <!--===============================================================================================-->	
	    <link rel="icon" type="image/png" href="images/icons/bus.ico"/>
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css">
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css">
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="vendor/animate/animate.css">
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css">
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="vendor/perfect-scrollbar/perfect-scrollbar.css">
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="css/util.css">
	    <link rel="stylesheet" type="text/css" href="css/main.css">
        <!--===============================================================================================-->
        </head>
        <div class="header">"""

        txRegistro+=f"""
        <h1>{titulo}</h1>
        """
        txRegistro+="""
        </div>
        <body>
	    <div class="limiter">
		<div class="container-table100">
		<div class="wrap-table100">
		<div class="table100 ver2 m-b-110">
		<div class="table100-head">
		<table>
		<thead>
		<tr class="row100 head">
        """
        for i in range(len(self.Claves)):
            txRegistro+=f"""<th class="cell100 column{i}">{self.Claves[i]}</th>"""
        txRegistro+="""
		</tr>
		</thead>
		</table>
		</div>
		<div class="table100-body js-pscroll">
		<table>
		<tbody>"""
        for j in range(len(self.Registros)):
            txRegistro+="""<tr class="row100 body">"""
            for k in range(len(self.Registros[j])):
                txRegistro+=f"""<td class="cell100 column{k}">{self.Registros[j][k]}</td>"""
            txRegistro+="""</tr>"""

        txRegistro+="""
		</table>
		</div>
		</div>
		</div>
		</div>
	    </div>
        <!--===============================================================================================-->	
	    <script src="vendor/jquery/jquery-3.2.1.min.js"></script>
        <!--===============================================================================================-->
	    <script src="vendor/bootstrap/js/popper.js"></script>
	    <script src="vendor/bootstrap/js/bootstrap.min.js"></script>
        <!--===============================================================================================-->
	    <script src="vendor/select2/select2.min.js"></script>
        <!--===============================================================================================-->
	    <script src="vendor/perfect-scrollbar/perfect-scrollbar.min.js"></script>
	    <script>
		$('.js-pscroll').each(function(){
		var ps = new PerfectScrollbar(this);
		$(window).on('resize', function(){
        ps.update();
		})
		});
			
		
	    </script>
        <!--===============================================================================================-->
	    <script src="js/main.js"></script>
        </body>
        </html>
        """
        Rhtml.write(txRegistro)
        Rhtml.close()
       

    def Generar_TablaTokens(self):
        tokenshtml=open(f'Tabla de Tokens/index.html','w')
        txtokens=''
        txtokens+="""
        <!DOCTYPE html> 
        <html lang="en">
        <head>
	    <title>Tabla de Tokens</title>
	    <meta charset="UTF-8">
	    <meta name="viewport" content="width=device-width, initial-scale=1">
        <!--===============================================================================================-->	
	    <link rel="icon" type="image/png" href="images/icons/favicon.ico"/>
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css">
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css">
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="vendor/animate/animate.css">
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css">
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="vendor/perfect-scrollbar/perfect-scrollbar.css">
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="css/util.css">
	    <link rel="stylesheet" type="text/css" href="css/main.css">
        <!--===============================================================================================-->
        </head>
        <div class="header">
        <h1>Tabla de Tokens</h1>
        </div>
        <body>
	    <div class="limiter">
		<div class="container-table100">
		<div class="wrap-table100">
		<div class="table100 ver1 m-b-110">
		<div class="table100-head">
		<table>
		<thead>
		<tr class="row100 head">
		<th class="cell100 column1">No.</th>
		<th class="cell100 column2">Token</th>
		<th class="cell100 column3">Lexema</th>
		<th class="cell100 column4">Fila</th>
		<th class="cell100 column5">Columna</th>
		</tr>
		</thead>
		</table>
		</div>
		<div class="table100-body js-pscroll">
		<table>
		<tbody>"""
        for ob in self.ListaTokens_T:
            if ob.lexema=='~' and ob.token=='Aceptacion':
                pass
            else:
                txtokens+=f"""<tr class="row100 body">
                <td class="cell100 column1">{ob.Numero}</td>
			    <td class="cell100 column2">{ob.token}</td>
			    <td class="cell100 column3">{ob.lexema}</td>
			    <td class="cell100 column4">{ob.fila}</td>
			    <td class="cell100 column5">{ob.columna}</td>
			    </tr>"""
        txtokens+="""
		</table>
		</div>
		</div>
		</div>
		</div>
	    </div>
        <!--===============================================================================================-->	
	    <script src="vendor/jquery/jquery-3.2.1.min.js"></script>
        <!--===============================================================================================-->
	    <script src="vendor/bootstrap/js/popper.js"></script>
	    <script src="vendor/bootstrap/js/bootstrap.min.js"></script>
        <!--===============================================================================================-->
	    <script src="vendor/select2/select2.min.js"></script>
        <!--===============================================================================================-->
	    <script src="vendor/perfect-scrollbar/perfect-scrollbar.min.js"></script>
	    <script>
		$('.js-pscroll').each(function(){
		var ps = new PerfectScrollbar(this);
		$(window).on('resize', function(){
        ps.update();
		})
		});
			
		
	    </script>
        <!--===============================================================================================-->
	    <script src="js/main.js"></script>
        </body>
        </html>
        """
        tokenshtml.write(txtokens)
        tokenshtml.close()
        
        #for x in self.ListaTokens:
        #    print(x.Numero,x.lexema,x.fila,x.columna,x.token)
        #
        #
    def Generar_TablaErrores(self):
        erroreshtml=open('Tabla de Errores/index.html','w')
        txtError=''
        txtError+="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
	    <title>Tabla de Errores</title>
	    <meta charset="UTF-8">
	    <meta name="viewport" content="width=device-width, initial-scale=1">
        <!--===============================================================================================-->	
	    <link rel="icon" type="image/png" href="images/icons/favicon.ico"/>
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css">
        <!--===============================================================================================-->
        <link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css">
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="vendor/animate/animate.css">
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css">
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="vendor/perfect-scrollbar/perfect-scrollbar.css">
        <!--===============================================================================================-->
	    <link rel="stylesheet" type="text/css" href="css/util.css">
	    <link rel="stylesheet" type="text/css" href="css/main.css">
        <!--===============================================================================================-->
        </head>
        <div class="header">
        <h1>Tabla de Errores</h1>
        </div>
        <body>
	    <div class="limiter">
		<div class="container-table100">
		<div class="wrap-table100">	
		<div class="table100 ver3 m-b-110">
		<div class="table100-head">
		<table>
		<thead>
		<tr class="row100 head">
		<th class="cell100 column1">Tipo de Error</th>
		<th class="cell100 column2">Caracter</th>
		<th class="cell100 column3">Descripción</th>
		<th class="cell100 column4">Fila</th>
		<th class="cell100 column5">Columna</th>
		</tr>
		</thead>
		</table>
		</div>
		<div class="table100-body js-pscroll">
        <table>
		<tbody>"""
        for a in self.ListaErrores:
            txtError+=f"""<tr class="row100 body">
			<td class="cell100 column1">{a.tipoError}</td>
			<td class="cell100 column2">{a.caracter}</td>
			<td class="cell100 column3">{a.descripcion}</td>
			<td class="cell100 column4">{a.filaError}</td>
			<td class="cell100 column5">{a.columnaError}</td>
			</tr>"""
        txtError+="""
        </tbody>
		</table>
		</div>
		</div>	
		</div>
		</div>
	    </div>
        <!--===============================================================================================-->	
	    <script src="vendor/jquery/jquery-3.2.1.min.js"></script>
        <!--===============================================================================================-->
	    <script src="vendor/bootstrap/js/popper.js"></script>
	    <script src="vendor/bootstrap/js/bootstrap.min.js"></script>
        <!--===============================================================================================-->
	    <script src="vendor/select2/select2.min.js"></script>
        <!--===============================================================================================-->
	    <script src="vendor/perfect-scrollbar/perfect-scrollbar.min.js"></script>
	    <script>
		$('.js-pscroll').each(function(){
		var ps = new PerfectScrollbar(this);
		$(window).on('resize', function(){
		ps.update();
		})
		});
	    </script>
        <!--===============================================================================================-->
	    <script src="js/main.js"></script>
        </body>
        </html>
        """
        erroreshtml.write(txtError)
        erroreshtml.close()
    







Aps=Application()
Aps.create_widgets()
Aps.root.mainloop()
