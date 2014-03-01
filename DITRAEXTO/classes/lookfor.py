#****************************************************
# MODULO DE BUSQUEDA
#****************************************************
class searchText:

    __numeroDelinea=0
    __texto=""
    __pathABuscar=""
    
    def __init__(self, textoABuscar, path):
        self.__texto=textoABuscar.strip()
        self.__pathABuscar = path
        
    def buscar(self):
        txt="FOUND in line number: {} in {} \n {}"
        print "Searching {}...".format(self.__texto)
        print "............................................"
        f=open(self.__pathABuscar+"tables_dic_vars.txt","r")
        g=open(self.__pathABuscar+"tables_dic.txt","r")

        for linea, linea2 in zip(f, g):
            if linea.find(self.__texto) >=0 or linea2.find(self.__texto) >=0:
                print "**********************************************************"
                print txt.format( self.__numeroDelinea, "tables_dic_vars.txt", linea) 
                print txt.format( self.__numeroDelinea, "tables_dic.txt", linea2)      
                self.__numeroDelinea+=1
            
        f.close()
        g.close()
