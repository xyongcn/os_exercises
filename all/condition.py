#coding=utf-8
#!/usr/bin/env python
  
import threading  
import time  
   
condition = threading.Condition()  
products = -1 
N = 10

class Producer1(threading.Thread):  
    def __init__(self):  
        threading.Thread.__init__(self)  
          
    def run(self):  
        global condition, products
        while True:  
            if condition.acquire():  
                if products == 0:  
                    condition.wait();  
                products = 0;  
                print "pick white"
                condition.notify()  
                condition.release()  

class Producer2(threading.Thread):  
    def __init__(self):  
        threading.Thread.__init__(self)  
          
    def run(self):  
        global condition, products
        while True:  
            if condition.acquire():  
                if products == 1:  
                    condition.wait();  
                products = 1;  
                print "pick black"
                condition.notify()  
                condition.release()    
if __name__ == "__main__":  
    p1 = Producer1()
    p1.start()
    p2 = Producer2()
    p2.start()