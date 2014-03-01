###############################################
#CREATED BY: DANYEL MORALES                   #
#FOR TESTING DIRECTORY TRAVERSAL VULNERABILITY#
###############################################
#VISIT: medennysoft.com                       #
#CONTACT ME: contacto@medennysoft.com         #
###############################################
from ErrorHandlerMod import ErrorHandler
from lookfor import searchText
import re
import os.path
import sys

class crawlerIt:
    __firstInclude=0 #false
    __objetoConf=""
    __nameConfigs=""
    __plantilla=""
    __libsPatrons=""
    __libsTables="libs/tables/"
    __engineSetUrl=[]

    #Manejadores de errores
    __ERRN=ErrorHandler()
    __NEAS=3 
    __NEAD=0
    __NEAD_Error=0

    
    #Auxiliar de archivos y carpetas
    __parentPath="" #Carpeta o nodo padre
    __cargarDeLista=None
    
    def __init__(self, objeto):
        self.__objetoConf=objeto
        self.__plantilla="files/"+self.__objetoConf.get_directorio()+"/"
        self.__libsPatrons=self.__objetoConf.get_libPatron()
        
    def __del__(self):
        print "Done!"

    #***************************************************
    #   Punto de entrada, se cargan targets desde lista,
    #   y conforme se usa se va eliminando.
    #
    #   Antes de usarse se crea el archivo
    #   correspondiente, y posteriormente
    #   brinca a analizarse para nuevas urls en includes.
    #*************************************************** 
    def principal(self):
        targets=open(self.__libsTables+"targets.txt","r")
        if self.__cargarDeLista==1:
            for checkingSourceWeb in targets:
                self.__engineSetUrl.append(checkingSourceWeb)
            self.typeTarg(self.__engineSetUrl[0], "w")
            self.__objetoConf.automaticListCD()
            targets.seek(0)
        
        for sourceWeb in targets:
            if sourceWeb!="":
                temp=sourceWeb
                archivo=(self.__plantilla+sourceWeb).strip("\r\n")
                sourceWeb=sourceWeb.strip("\r\n")

                if self.__firstInclude==0:
                    self.__firstInclude=1
                else:
                    self.__parentPath=sourceWeb=self.createFiles(sourceWeb)
                    if self.__objetoConf.get_status()=="ERROR":
                        self.deleteItemBuffer(temp)
                        self.eliminarLinea()
                        targets.seek(0)
                        continue
                            
                value=self.__ERRN.Error_ExistsDir(self.__libsPatrons)
                if value==1:
                    try:
                        KeySourceCode=open(self.__plantilla+sourceWeb, 'r')
                        for lineas in KeySourceCode:
                            lineas=lineas.strip(" ")
                            self.cargador_configs(lineas)
                            self.XtractMiddleText(lineas)
                            #****Comparamos en busca de vars****
                            if self.replaceVars(lineas,1)=="ERR4":
                                self.replaceVars(lineas,0)
                            #***********************************
                        KeySourceCode.close()
                    except:
                        print self.__ERRN.Chk_Err(self.__ERRN.Error_CantOpenSourceWeb() , sourceWeb)
                        #continue
                else:
                    print self.__ERRN.Chk_Err(value , self.__libsPatrons)
                    print self.__ERRN.Chk_Err(self.__ERRN.Error_NotExistsPatern() , self.__objetoConf.get_fileType())
                    self.__engineSetUrl.append("")
          
                self.eliminarLinea()
                targets.seek(0)
                
        self.lookfor()
        self.moveLogFiles()
        targets.close()

    def typeTarg(self, palabra, mode):
        target=open(self.__libsTables+"targets.txt",mode)
        target.write(palabra.strip("\r\n"))
        target.close()
        
    def lookfor(self):
        print "\n Dxtra says: \"I did what i could, you should continue by your own.\""
        answ=raw_input('\nDo you want to search in logs? y/n: ')
        varTemp=0
        while varTemp==0:
            if answ == "y":
                varTemp=1
                search=raw_input("What do you want to search?: ") #For python 2.7, not for python 3
                res=searchText(search, self.__libsTables)
                res.buscar()
                self.lookfor()
            elif answ == "n":
                varTemp=1
                print "**********************************************************"
                print "                         FINISHED                         "
                print "**********************************************************"
                #break
            else:
                print "Invalid option, try again."
                answ=raw_input('\nDo you want to search in logs? y/n: ')
                
    def moveLogFiles(self):
        self.__objetoConf.set_path("files/"+self.__objetoConf.get_directorio())
        self.__objetoConf.set_FileM(self.__libsTables+"tables_dic_vars.txt")
        self.__objetoConf.moveFile(2)  
        self.__objetoConf.set_FileM(self.__libsTables+"tables_dic.txt")
        self.__objetoConf.moveFile(2)
                                    
    def replaceVars(self, linea, opc):
        linea=self.filtrarPalabrasReservadas(linea.strip(" "))
        diccionario=open(self.__libsTables+"tables_dic_vars.txt", 'a+')
        patronVars=open(self.__libsPatrons + "patronVars.txt","r")
        if opc==0 or opc==1 or opc==12: #guarda o verifica
            for lineas in patronVars:
                lineas=lineas.strip()
                left=lineas.split("*")[0]
                center=lineas.split("*")[1]
                right=lineas.split("*")[2]
                posible=lineas.split("*")[3]
                if opc==0: #guarda                    
                    linea=self.eliComDerecha(linea,right)
                    linea=self.eliComIzq(linea,left,right)
                    linea=self.textoEnmedio(linea, left, right) + "="
                    #***************************************************************************
                    declaracion=linea.split("=")[0].strip()
                    definicion=linea.split("=")[1].strip()
                    string1 = self.filtrar(left+declaracion+"****"+definicion+"****")
                    string2 = self.filtrar(posible+declaracion+"****"+definicion+"****")
                    diccionario.write(string1+ "\n")
                    diccionario.write(string2+ "\n")                                   
                    #***************************************************************************
                elif opc==1: # verifica
                    if linea.find(left) >= 0 and linea.find(center) >= 0 and linea.find(right) >= 0:
                        return "ERR4"
                    else:
                        return 1
                    
                elif opc==12: # verifica antes reemplazo
                    if linea.find(left) >= 0 and linea.find(posible) >= 0:
                        return "ERR4"
                    else:
                        return 1
                    
            patronVars.close()
        elif opc== 2: #reemplaza
            for v in diccionario:
                wordToSearch=linea
                if wordToSearch.find(v.split("****")[0]) >= 0:
                    linea=linea.replace(v.split("****")[0],v.split("****")[1])
                    return linea
        diccionario.close()
    
    def eliComDerecha(self,lineal, patronFinal):
        pos=lineal.index(patronFinal)
        lineal=lineal[0:pos+1]
        return lineal
    
    def eliComIzq(self,lineal, patronInicial,patronFinal):
        pos=lineal.index(patronInicial)
        if pos>0:
            pos-=1
        pos2=lineal.index(patronFinal)+1
        lineal=lineal[pos: pos2]
        return lineal    
    
    def XtractMiddleText(self, lineaSourceWeb):
        try:
            lineas=lineaSourceWeb
            KeySourcePatrons=open(self.__libsPatrons+"patronCrawler.txt", 'r')
            for patrones in KeySourcePatrons:
                left=patrones.split("*")[0]
                right=patrones.split("*")[1]
                if lineas.find(left) >= 0 and lineas.find(right) >= 0:
                    newUrl=(self.textoEnmedio(lineas,left,right)).strip("\r\n")
                    if newUrl.find('\(') >=0 or newUrl.find('=') >=0 or  newUrl.find(';') >=0 or  newUrl.find('{') >=0:
                        continue
                    else:
                        newUrl=self.setParentPath(newUrl.strip(" "), self.__parentPath) #Agrega el directorio padre
                        self.__engineSetUrl.append(newUrl.strip(" "))
                    
            KeySourcePatrons.seek(0)
            KeySourcePatrons.close()     
        except:
            self.__NEAD+=1

    #Carga constantes declaradas
    def cargador_configs(self, lineasWebConf):
        try:
            lineas=lineasWebConf
            configPatrons=open(self.__libsPatrons+"patronDefinitions.txt", 'r')
            diccionario=open(self.__libsTables+"tables_dic.txt", 'a+')
            lineas=self.filtrarPalabrasReservadas(lineas.strip(" "))
            for patrones in configPatrons:
                left=patrones.split("*")[0].strip(" ")
                right=patrones.split("*")[4].strip(" ")
                center=patrones.split("*")[2].strip(" ")
                if lineas.find(left) >= 0 and lineas.find(right) >= 0:
                    word=(self.textoEnmedio(lineas, left, right).strip("\r\n")+ center.strip("\r\n"))
                    string = (self.filtrar((word.split(center)[0] +"****"+ word.split(center)[1]+"****")))
                    diccionario.write(string.strip(" ").lstrip() + "\n")
            configPatrons.seek(0)       
            configPatrons.close()
        except:
            pass
        
    #Se encarga de agregar el directorio padre si es necesario
    def setParentPath(self, target, parent):
        countParent=parent.count("/")
        contador=0
        carpeta=""
        if target.count("/")==0 and countParent==0:
            target=target
        elif target.count("/")==0 and countParent > 0:
            while contador != countParent:
                mo=parent.split("/")[contador]
                carpeta +="/" + mo
                contador+=1
            target=carpeta+"/"+target
        
        return target
    
    #Elimina target ya usado y corre la lista al siguiente
    def eliminarLinea(self):
        targets=open(self.__libsTables+"targets.txt", "w+")
        bufferTxt=""
        try:
            targets.write(self.__engineSetUrl[0])
        except:
            pass
        targets.close()
        self.moverEspaciosEnBuffer(0)
        
    def deleteItemBuffer(self, item):
        tempList=self.__engineSetUrl
        self.__engineSetUrl=[]
        for i in range(len(tempList)-1):
            if tempList[i]!=item:
                self.__engineSetUrl.append(tempList[i])
        
    #Mueve espacios en lista ya sea para eliminar o para
    #Mover un target del principio al final.
    def moverEspaciosEnBuffer(self, opc):
        if opc==0: #Eliminar target
            for i in range(len(self.__engineSetUrl)-1):
                self.__engineSetUrl[i]=self.__engineSetUrl[i+1]

        if opc==1: #mandar a lo ultimo 
            temp_0=self.__engineSetUrl[0]
            ultimo=len(self.__engineSetUrl)
            for i in  range(len(self.__engineSetUrl)-1):
                self.__engineSetUrl[i]=self.__engineSetUrl[i+1]
            self.__engineSetUrl[ultimo-1]=temp_0

    #Extrae el texto entre dos patrones delimitantes.       
    def textoEnmedio(self, linea, delimitterLeft, delimitterRight):     
        palabra=linea
        palabra=(palabra.replace(delimitterLeft, "")).strip()
        palabra=(palabra.replace(delimitterRight,"")).strip()
        return  palabra

    #Filtramos caracteres no deseados.
    def filtrar(self, palabra):
        palabra=palabra.replace("'", "").replace("\"", "").replace(",","").replace(";","").strip(" ").strip("\r\n").lstrip()

        if palabra.find(r"../")>=0:
            palabra=self.filtrarDotDotSlash(palabra)
        else:
            palabra=palabra.replace(r"/.","").replace(r"./","").replace(r" . ","").replace(r". / ","/")
        return palabra

    def filtrarDotDotSlash(self, palabra):
        if palabra.split("/")[0]=="":
            palabra=palabra.replace("/","",1)

        c=palabra.count("./")
        counter=0
        acumulador=""
        stringOriginal=""
        if c > 0:
            while counter != c:
                mo=palabra.split("./")[counter]
                if mo==".":
                    acumulador+="../"
                    stringOriginal+="../"
                else:
                    stringOriginal+="./"
                counter+=1
                
        palabra=acumulador+(palabra.replace(stringOriginal,"").strip())
        return palabra
    
    #Filtramos palabras reservadas que danien la linea
    def filtrarPalabrasReservadas(self, lineas):
        patron = open (self.__libsPatrons+"patronReservedWords.txt","r")
        for patrones in patron:
            if lineas.find(patrones.split("*")[0]) >= 0 :
                lineas=lineas.replace(patrones.split("*")[0],"")
                lineas=lineas.replace(patrones.split("*")[1],"")
        patron.close()
        return lineas

    #Dropea una linea
    def drop_targ(self):
        self.saveFile(" ", 'w')

    #Creamos un archivo con filtrado y reemplazo de constantes.
    def createFiles(self,sitio):
        try:
            datoToSave=self.filtrar(sitio)
            datoToSave=self.filtrar(self.takeOffWordByDef(datoToSave))
            #****Comparamos en busca de vars****
            if self.replaceVars(datoToSave,12)=="ERR4":
                 datoToSave=self.replaceVars(datoToSave,2)
            #***********************************
            datoToSave=self.takeOffWordByDef(datoToSave).strip()
            sitio=self.__objetoConf.createSingleFile(datoToSave)
            return sitio
        except:
            #Si ocurre este error posiblemente se deba a que se detecto una variable
            print "Error en " + sitio

    #Guardamos un archivo en targets, se le pasa modo y la linea a guardar.    
    def saveFile(self, filex, modo):
        target=self.__libsTables+"targets.txt"
        if os.path.exists(target) and os.path.isfile(target) or modo=='a+':
            FileToSaveUrl = open(target, modo)
            FileToSaveUrl.seek(0)
            FileToSaveUrl.write("\n"+filex.lstrip().strip("\r\n"))
            FileToSaveUrl.close()

    #Se encarga de sustituir palabras de constantes en las lineas.
    def takeOffWordByDef(self, palabra):
        wordToSearch=palabra
        diccionario=open(self.__libsTables+"tables_dic.txt", "r")
        for v in diccionario:
            if wordToSearch.find(v.split("****")[0]) >= 0:
                palabra=palabra.replace(v.split("****")[0],v.split("****")[1])  
        diccionario.close()
        return palabra

    def createTempUrl(self,palabra, modo):
        self.drop_targ()
        self.saveFile(palabra, modo)
        self.createFiles()
        self.drop_targ()

    def filtrarFirstSlash(self, palabra):
        palabra=palabra.replace("/", "", 1)
        return palabra

    def set_cargarDeLista(self, opc):
        self.__cargarDeLista=opc
        
    def get_cargarDeLista(self):
        return self.__cargarDeLista
