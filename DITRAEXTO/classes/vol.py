import random
import os
class randomImage:
    def __init__(self):
        os.system('cls') #windows use os.system('clear') for Linux
        number = random.randint(0, 1)
        self.image(number)
        print("This tool is created by Daniel Morales".center(80))
        print ("danielmorales@tugaloper.com".center(80))
        
    def image(self, number):

        if number==0:
                   print ('''
                 _____ 
                _|[]_|_                                                 
              _/_/=|_\_\_            
            _/_ /==| _\ _\_                             
          _/__ /===|_ _\ __\_                                           
        _/_ _ /====| ___\  __\_     
      _/ __ _/=====|_ ___\ ___ \_                                       
    _/ ___ _/======| ____ \_  __ \_ 
                          ''')
        elif number==1:
                   print ('''
                
                                     ,ood8888booo,
                                  ,od8'         `8bo,
                               ,odP                 Ybo,
                             ,d8'                     `8b,
                            ,oP                         Yo,
                           ,8                             8,
                           8Y                             Y8
                           8l                   aba       l8
                           Ya               ,ad'  8       aY
                            Y8,           aY8,   ,P     ,8Y
                             Y8o          aP     8     o8Y
                              `Y8      ,aP'      8    8Y'
                      ,arooowwwwwooo88P'        d'  aY'
                   ,adP                        ,aa8P
                  aP  a8a,                     d'
                 $       Y          ,    ,    ,8
                $  $,    P     a8888b   daaa  8
               $  $ Y  aP 8  ad      8  8   8 `a
               $ $  8 8  d  P        d ,P   `8 8
               `$'  d 8  `8 ba       Y 8     `8 ba
                    8  ba  8a$       8  ba    `8a$
                     Yaa$             Yaa$
                          ''')                   
