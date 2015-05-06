#coding=utf-8
import threading  
import random  
import time  
frame = 0
wheel = 0
N = 10

class SemaphoreThread1(threading.Thread):  
    def __init__(self,threadName,s1,s2):  
       threading.Thread.__init__(self,name=threadName)  
       self.s1 = s1
       self.s2 = s2
    def run(self):  
      """Print message and release semaphore"""  
      while True: 
        self.s1.acquire()  
        print "pick write\n"
        self.s2.release()
      #self.threadSemaphore.release()  

class SemaphoreThread2(threading.Thread):  
    def __init__(self,threadName,s1,s2):  
       threading.Thread.__init__(self,name=threadName)  
       self.s1 = s1
       self.s2 = s2
    def run(self):  
      """Print message and release semaphore"""  
      while True: 
        self.s2.acquire()  
        print "pick black\n"
        self.s1.release()           
        
#semaphore allows five threads to enter critical section  
s1=threading.Semaphore(1)  
s2=threading.Semaphore(1)  
p1 = SemaphoreThread1("p1",s1,s2)
p1.start()
p2 = SemaphoreThread2("p2",s1,s2)
p2.start()