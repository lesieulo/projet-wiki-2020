# Python 3 program to demonstrate subprocess  
# module 
  
import subprocess 
import os 
  
def excuteC(): 
  
    # store the return code of the c program(return 0) 
    # and display the output 
    s = subprocess.check_call("gcc HelloWorld.c -o out1;./out1", shell = True) 
    print(", return code", s) 

# Driver function 
if __name__=="__main__": 
    excuteC()   
