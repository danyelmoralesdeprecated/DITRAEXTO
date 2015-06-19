###############################################
#CREATED BY: DANYEL MORALES                   #
#FOR TESTING DIRECTORY TRAVERSAL VULNERABILITY#
###############################################
#VISIT: blog.tugaloper.com                 
#CONTACT ME: danielmorales@tugaloper.com
###############################################
from ErrorHandlerMod import ErrorHandler
import os
import shutil
import re
import time

class globalConfigs:
    __directorio=''
    __fileM=''  #nombre del archivo armado
    __type='' #Tipo de archivo
    __indexFolder=0    
    __otherPath='files/' #Almacena las direcciones de carpetas que se crearan
    __dominio=""

    #Temp var
    __pathVuln=""
    
    #****PATRONES****
    __patronInicio='' #Delimiter at the top, patron
    __patronFinal=''  #Delimiter at the bottom, patron
    
    __objetoExterno=''
    __libsPatrons="libs/patrons/"
    __libsTables="libs/tables/"
    
    __ERRNO=""
    __ERRTEMP=0
    
    def __init__(self, directorio, nombre, tipo):
        self.__dominio=self.__directorio=directorio
        self.__fileM=nombre + '.'+ tipo
        self.__type=tipo
        #self. __libsPatrons+=self.__type+"/"
        
    def __del__(self):
        print "Done!"
        
    def createDirectory(self):
        directorio = os.path.join(self.__otherPath, self.__directorio)
        if not os.path.isdir(directorio):
            os.mkdir(directorio)
            
    def moveFile(self, opc):
        dirFile=""
        try:
            if opc==1:  #move Single File
                dirFile='files/'+self.__directorio
            elif opc==2: #moveFileList
                dirFile=self.__otherPath
            else:
                print "Invalid option"

            shutil.move(self.__fileM, dirFile)
            self.set_status("Ok")
        except:
            self.set_status("ERROR")
            print "Error Moving: " + self.__fileM
            try:
                os.remove(self.__fileM)
            except:
                pass
            
        
    def deleteTemp(self):
        try:
            xfile=('temporal.'+self.__type).rstrip("\r\n")
            os.remove(xfile)
        except:
            pass
    
    def automaticListCD(self):
        tempName="" #Almacena el ultimo directorio creado para roll back
        directorioPat=self.__directorio
        self.__otherPath+= directorioPat
        
        contador = 0
        carpeta=""
        
        f = open(self.__libsTables+"targets.txt", "r")
        for linea in f:
            while contador != linea.count("/"):
                try:
                    mo=linea.split("/")[contador]
                    self.__directorio=mo
                    self.createDirectory()
                    self.__otherPath+="/" + self.__directorio
                    contador+=1
                    carpeta +="/" + mo
                except:
                    print "Error creando archivo..."
            #*****************************************
            self.deleteTemp()
            fileNameToSource=linea.split("/")[contador]
            tempName=carpeta
            try:
                self.extractSourceList(fileNameToSource, carpeta)
                self.__fileM=fileNameToSource.rstrip("\r\n")
                self.__otherPath+="/"
                self.moveFile(2)
            except:
                try:
                    os.remove(tempName)
                    self.tryToReparList()
                    self.automaticListCD()
                    break
                except:
                    print "Espere..."
            time.sleep(2)
            #*****************************************
            contador=0
            carpeta=""
            self.__otherPath = 'files/' + self.get_directorio()  #directorioPat
        f.close()

    def tryToReparList(self):
        f = open(self.__libsTables+"targets.txt", "r")
        temporal=[]
        counter =0
        
        for fuente in f:
            temporal.append(fuente.strip(" ").strip("\r\n").strip(""))
        f.close()
        
        largoList=temporal.__len__()
        
        g = open(self.__libsTables+"targets.txt", "w")
        while counter != largoList:
            if counter !=0 and counter < largoList-1:
                g.write(temporal[counter].strip("\r\n") + "\n")
            else:
                g.write(temporal[counter].strip("\r\n"))
            counter +=1
        g.close()

    def createSingleFile(self, linea):
        contador=0
        carpeta=""
        self.__otherPath='files/'+self.get_directorio()
        #************************************
        #Soluciona el problema de carpetas ../
        temp=linea
        linea=linea.replace(r"../","").strip()
        #************************************
        while contador != linea.count("/"):
                try:
                    mo=linea.split("/")[contador]
                    self.__directorio=mo
                    self.createDirectory()
                    self.__otherPath+="/" + self.__directorio
                    contador+=1
                    carpeta +="/" + mo
                except:
                    print "Error al crear directorios..."
        self.deleteTemp()
        fileNameToSource=linea.split("/")[contador]
        #*****************************************
        #Solucionamos el problema de carpetas ../
        #*****************************************
        if temp.find(r"../")>=0:
            numDotDotSlash=temp.count(r"../")
            acumulador=""
            for i in range(numDotDotSlash):
                acumulador+="/.."
            carpeta=(acumulador+carpeta).strip()
        #******************************************
        self.extractSourceList(fileNameToSource,carpeta) #/ require
        self.__fileM=fileNameToSource.rstrip("\r\n")
        self.__otherPath+="/"
        self.moveFile(2)
        return linea
    
    def extractSourceList(self, fileNameToSource, pathVulnToSource):           
        countDot=fileNameToSource.count(".")
        name=""
        if countDot > 1:              
            filetyp=fileNameToSource.split(".")[countDot]
            mo = re.match("(.+)\.", fileNameToSource)
            name=mo.group(1)
        else:
            name=fileNameToSource.split(".")[0]
            filetyp=fileNameToSource.split(".")[1]
        
        self.__type=filetyp    
        objExploit=self.__objetoExterno
        objExploit.set_name(name.rstrip("\r\n"))
        objExploit.set_filetyp(filetyp.rstrip("\r\n"))
        objExploit.set_pathVulnToSource(pathVulnToSource.rstrip("\r\n"))
        objExploit.startConnection()
   
    def set_objeto(self, obj):
        self.__objetoExterno=obj
        
    def set_pathVuln(self, path):
        self.__pathVuln=path
        
    def get_pathVuln(self):
        return self.__pathVuln
    
    def get_path(self):
        return self.__otherPath

    def set_path(self, path):
        self.__otherPath=path
    
    def get_directorio(self):
        return self.__dominio
    
    def get_libTables(self):
        return self. __libsTables
    
    def get_libPatron(self):
        return self. __libsPatrons

    def get_fileType(self):
        return self.__type
    
    def set_FileM(self, fileM):
        self.__fileM=fileM
        
    def get_FileM(self):
        return self.__fileM
        
    def set_status(self, status):
        self.__ERRNO=status
        
    def get_status(self):
        return self.__ERRNO
        
    def set_patern(self, patronInicie, patronFinale):
        self.__patronInicio=patronInicie
        self.__patronFinal=patronFinale
        
    def single_Set(self):      
        self.__objetoExterno.set_pathVulnToSource(self.__pathVuln)
        self.__objetoExterno.startConnection()             
        self.moveFile(1)
    
    def set_delimiter(self, choose):
        self.__objetoExterno.set_choose(choose)
        nLines=0
        #*************FROM A FILE ***********
        if choose==0:
            try:
                f = open(self.__libsPatrons+"delimiters.txt", "r")
                for linea in f:
                    if  self.__type == linea.split("_")[0]:
                        self.__objetoExterno.set_patern(linea.split("_")[1], linea.split("_")[2])
                    else:
                        self.__ERRTEMP+=1
                    nLines+=1
                f.close()

                if self.__ERRTEMP == nLines:
                    print ":( Patern not found..."
            except:
                print "Error abriendo archivo."
        #*************FROM DELIMITERVAR***********
        if choose==1:
            self.__objetoExterno.set_patern(self.__patronInicio , self.__patronFinal)
        
        #*************FROM USER***********
        if choose==2:
            self.__objetoExterno.set_patern(self.__patronInicio , self.__patronFinal)

        #Updating the value of this variable.
        self.__libsPatrons+=self.__type+"/"
