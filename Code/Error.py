class Error:
    def __init__(self,tipo,fila,columna,descripcion,caracter):
        self.tipoError=tipo
        self.filaError=fila
        self.columnaError=columna
        self.descripcion=descripcion
        self.caracter=caracter