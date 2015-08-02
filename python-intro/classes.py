# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 23:16:50 2015

@author: patrickchrist
"""

class Student:
    immatriculation=True  
    def __init__(self, name, major, age): # Method is called when an object is initiated      		
        self.name = name      
        self.major = major      
        self.age = age      
    def study(self):     
        print 'I am', self.name, 'and I am studying', self.major   
    def drinking(self, drink):      
        print 'I am', self.name, 'and I am drinking', drink
        
## Creation of new Objects
Patrick = Student('Patrick', 'Physik', '26')
Laura = Student('Laura', 'Sustainability Studies', '27')

## Calling Methods

Patrick.study()
Patrick.drinking('Tegernseer')
Laura.drinking('Tea')
print Patrick.age


## Inheritance
class PhDStudent(Student):    
    def __init__(self, doc_father, name, major, age):            
        Student.__init__(self, name, major, age)      		        
        self.doc_father = doc_father    
    def teaching(self, course_name):        
        print "I am", self.name, "and I am teaching", course_name

Patrick_CA=PhDStudent('Bjoern Menye', 'Patrick','Physik', '26')
Patrick_CA.doc_father
Patrick_CA.teaching('Drone Elective')
Patrick_CA.study()