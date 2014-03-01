class encodeString:

    __String=""
    __dot="%2e"
    __slash="%2f"
    __backSlash="%5c"
    __opc=None
    
    def __init__(self, string, opc):
        self.__String=string
        self.__opc=opc
        
    def selectCase(self):
        if self.__opc==0:
            return self.dotEdotEslashE()  #%2e%2e%2f
        elif self.__opc==1:
            return self.dotEdotEslash()   #%2e%2e/  o %2e%2e\
        elif self.__opc==2:
            return self.dotdotslashE()    #..%2f
        elif self.__opc==3:
            return self.dotEdotEBackSlashE() # %2e%2e%5c
        elif self.__opc==4:
            return self.dotdotBackSlashE()  #..%5c
        elif self.__opc==5:
            return self.returnNormal()  #with out encoding
        else:
            return self.returnNormal()

    def returnNormal(self):
        return self.__String
    
    def dotEdotEslashE(self):
        string=self.__String.replace("/",self.__slash).replace(".",self.__dot)
        return string

    def dotEdotEslash(self):
        string=self.__String.replace(".",self.__dot)
        return string
    
    def dotdotslashE(self):
        string=self.__String.replace("/",self.__slash)
        return string
    
    def dotEdotEBackSlashE(self):
        string=self.__String.replace("\\",self.__backSlash).replace(".",self.__dot)
        return string
    
    def dotdotBackSlashE(self):
        string=self.__String.replace("\\",self.__backSlash)
        return string
