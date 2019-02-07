
import sympy
import numpy
import random
import time
import matplotlib.pyplot

class cryptography_algorithm(object):

    def __init__(self,plaintext,cybertext):
        self.plaintext =  plaintext 
        self.cybertext = cybertext

    def encryption(self):
         pln = self.str2lst(self.plaintext)
         cphr =self.R_function(pln,True)
         self.cybertext = self.lst2str(cphr)
         
    def decryption(self):
         cphr = self.str2lst(self.cybertext)
         pln = self.R_function(cphr,False)
         self.plaintext = self.lst2str(pln)

    def R_Function(self):
        return 0

    # The function str2lst accepts a string  and returns its arithmetic coding to ASCI

    def lst2str(self,list):
        return ''.join([chr(x+65) for x in list])

    # The function lst2str receives a list of numbers and returns an alphanumeric

    def str2lst(self,string):
         return [ord(x) - 65 for x in string]


class asymetric_algorithm(cryptography_algorithm):

    def __init__(self, plaintext, cybertext, public_key, private_key): 
                self.public_key = public_key 
                self.private_key= private_key 

                # invoking the __init__ of the parent class  
                cryptography_algorithm.__init__(self, plaintext, cybertext)  


class symetric_algorithm(cryptography_algorithm):

     def __init__(self, plaintext, cybertext, public_key): 
                # invoking the __init__ of the parent class  
                cryptography_algorithm.__init__(self, plaintext, cybertext)  
                self.public_key = public_key 


     
class Shift_Chipher(symetric_algorithm):
    

     def __init__(self, plaintext, cybertext, public_key):
           # invoking the __init__ of the parent class 
           symetric_algorithm.__init__(self,plaintext,cybertext,public_key)

   
     def R_function(self,text,encrypt):

           if encrypt :
               txt = [(x + self.public_key ) % 26 for x in text]
               
           else :
               txt = [(x - self.public_key) % 26 for x in text]

           return txt
             
       
       
class Affine_Chipher(symetric_algorithm):
    

     def __init__(self, plaintext, cybertext, public_key):
           # invoking the __init__ of the parent class 
           symetric_algorithm.__init__(self,plaintext,cybertext,public_key)

                  
    

     def R_function(self,text,encrypt):

           if encrypt :
                txt = [ self.public_key[0] * x  + self.public_key[1]  % self.public_key[2] for x in text]
               
           else :
               txt = [(sympy.mod_inverse(self.public_key[0],self.public_key[2]) * (x - self.public_key[1])) % self.public_key[2] for x in text]

           return txt


class Subsistition_Chipher(symetric_algorithm):
    
    
     def __init__(self, plaintext, cybertext, public_key):
           # invoking the __init__ of the parent class 
           symetric_algorithm.__init__(self,plaintext,cybertext,public_key)

                 
     def R_function(self,text,encrypt):

           alphabet = 'abcdefghijklmnopqrstuvwxyz.,! '
        
           if encrypt :
               keyMap = dict(zip(alphabet, self.public_key))
               txt = self.str2lst(''.join(keyMap.get(c.lower(), c) for c in self.lst2str(text)))

               
           else : 
                keyMap = dict(zip(self.public_key, alphabet))
                txt = self.str2lst(''.join(keyMap.get(c.lower(), c) for c in self.lst2str(text)))

            
           return txt

     
class RSA(asymetric_algorithm):
    
     def __init__(self, plaintext, cybertext, public_key,private_key):
           # invoking the __init__ of the parent class 
           asymetric_algorithm.__init__(self,plaintext,cybertext,public_key,private_key)



     def R_function(self,text,encrypt):

           if encrypt :
                 txt = [pow(char, self.public_key[1],self.public_key[0]) for char in text]
                
           else : 
                 txt = [pow(char, self.private_key[1],self.private_key[0]) for char in text]
                
           return txt
           
 

def main():

    message =str(input("Enter the message : "))
    handler = Handler(message,[])
    handler.Calculate_Times()
    handler.printResults()
   
    
    return

class Handler():
     

     def __init__(self, plaintext,timeList): 
         self.plaintext=plaintext
         self.timeList = timeList
     

     def Run(self,cryptography_algorithm):
         cryptography_algorithm.encryption()
         cryptography_algorithm.decryption()

     def printResults(self):
        
         matplotlib.pyplot.scatter(self.timeList,["Shift","Affine","Subsistition","RSA"])
         matplotlib.pyplot.show()

     def Calculate_Times(self):

         key_generator = Key_Generator()

         start = time.clock()
         public_key = key_generator.SC_Generator()
         shf = Shift_Chipher(self.plaintext,"",public_key)
         self.Run(shf)
         stop = time.clock()
         self.timeList.append((stop-start)*100)


         start = time.clock()
         public_key = key_generator.AC_Generator(8)
         shf = Affine_Chipher(self.plaintext,"",public_key)
         self.Run(shf)
         stop = time.clock()
         self.timeList.append((stop-start)*100)

         start = time.clock()
         public_key = key_generator.SUC_Generator()
         shf = Subsistition_Chipher(self.plaintext,"",public_key)
         self.Run(shf)
         stop = time.clock()
         self.timeList.append((stop-start)*100)


         start = time.clock()
         public_key , private_key = key_generator.RSA_Generator(1024)
         shf = RSA(self.plaintext,"", public_key , private_key)
         self.Run(shf)
         stop = time.clock()
         self.timeList.append((stop-start)*100)





class Key_Generator():


     #implement  Subsistition_Chipher key generator 

     def SUC_Generator(self):

          l = numpy.random.permutation(29)
          string_list = list('abcdefghijklmnopqrstuvwxyz.,! ')
          perm = ''.join([ string_list[l[i]] for i in l ])
    
          return perm




     #implement Shift_Chipher key generator
     def SC_Generator(self):

        return random.randint(1,25)




     #implement Affine_Chipher key generator
     def AC_Generator(self,keySize):

        #Step 1 choose one random number from 1 to KeySize 
       
        key_2 = random.randint(1,keySize)

        #Step 2 choose one random number from KeySize + 1  to 2^KeySize

        n = random.randint(keySize + 1 , pow(2,keySize))

        #Step 3 choose  one number that is coprime with n 

        key_1 = sympy.randprime(1 , pow(2,keySize))

        public_key = ( key_1 , key_2  , n )
        
        return  public_key




     #implement RSA key generator

     def RSA_Generator(self , keySize):

        # Creates a public/private key pair with keys that are keySize bits in
        # size. This function may take a while to run.
 
        # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
        p = sympy.randprime(0,keySize)
        q = sympy.randprime(0,keySize)
        n = p * q
        phi = (p-1)*(q-1)
 
        # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
        e = sympy.randprime(1,phi)
 
        # Step 3: Calculate d, the mod inverse of e.
        d = sympy.mod_inverse(e, phi)
       
   
        publicKey = (n,e)
        privateKey = (n,d)


        return publicKey , privateKey 
 


if __name__ == '__main__':
    main()
