###############################################
#CREATED BY: DANYEL MORALES                   #
#FOR TESTING DIRECTORY TRAVERSAL VULNERABILITY#
###############################################
#VISIT: codedevelopers.hol.es                 #
#CONTACT ME: medennysoft@outlook.com          #
####################################################
#    helpXtra - building urls using methods.       #
####################################################
import argparse
import sys
sys.path.append("classes/")
from vol import randomImage
class cleaningMetods:

    __palabra=""
    __replaceInKey=""
    __libsPatrons="libs/patrons/"
    __libsTables="libs/tables/targets.txt"
    
    def __init__(self):
        image=randomImage()
        self.principal()

    def main():
        pass

    def principal(self):
        parser = argparse.ArgumentParser(description='This tool will help you to build urls using methods and arguments.'+
                                         ' You need to write into irregular.txt the methods with arguments.',
                                         epilog='Ej: base -> "/classes/$varname.php"  key->"$varname"')
        parser.add_argument("-b","--base",type=str, help="The base string where will be replaced the key string.", required=True)
        parser.add_argument("-k","--key",type=str, help="The key string who will be replaced in base string.",required=True)
        args = parser.parse_args()
        
        self.__palabra=self.replacer(args.base)
        self.__replaceInKey=self.replacer(args.key)
        g=open(self.__libsTables, "a")
        for ls in self.values():
            g.write(ls + "\n")
        g.close()
        print "Done!"
        
    def values(self):
        f=open(self.__libsPatrons+"irregular.txt","r")
        for linea in f:
            left=linea.split("(")[0]
            right=linea.split(")")[1]
            foo=self.replacer(linea.replace(left,"").replace(right,""))
            bar=self.replacer(self.__palabra.replace(self.__replaceInKey,foo))
            yield bar
        f.close()

    def replacer(self, palabra):
        palabra=palabra.replace(r"'", "").replace(r")", "").replace(r"(", "").replace(r"\"", ""+
                                "").replace(r" . ","").replace(r",","").replace(r";","").strip().strip("\r\n").lstrip()
        return palabra

if __name__=='__main__':
    ojPrincipal=cleaningMetods()
