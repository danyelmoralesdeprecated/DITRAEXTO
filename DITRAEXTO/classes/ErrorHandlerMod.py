import os.path
class ErrorHandler:

    def __init__(self):
        pass

    def Chk_Err(self, opc, arg):
        if opc=="ERR0":
            print "The File does  not exist, Error in: " + arg
        elif opc=="ERR1":
            print "The dir does not exist, Error in: " + arg
        elif opc=="ERR2":
            print "The file Cannot be open. Does this file really exist?, Error in: " + arg
        elif opc=="ERR3":
            print "The patern does not exist. Error in: " + arg
        elif opc=="ERR4":
            print "An invalid character was found. Error in: " + arg
        elif opc=="ERR5":
            print "A variable was detected on the line. Error in: " + arg
        else:
            print "Invalid option"
            
    def Error_ExistsFile(self, path):
        if os.path.isfile(path):
            return  1 #It exists
        else:
            return  "ERR1" #Does not exist 
        
    def Error_ExistsDir(self, path):
        if os.path.isdir(path):
            return  1 #It exists
        else:
            return  "ERR1" #Does not exist 
        

    def Error_CantOpenSourceWeb(self):
        return "ERR2"

    def Error_NotExistsPatern(self):
        return "ERR3"
    
    def Error_FindCharacter(self, site):
        return  "ERR4"
        
    def Error_VariableDetected(self):
        return "ERR5"
