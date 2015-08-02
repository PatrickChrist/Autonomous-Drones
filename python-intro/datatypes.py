# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 21:44:31 2015

@author: patrickchrist
"""
## Part I
beers_yesterday = 5 		# An integer assignment 
liters_beers_yesterday = 2.5 		# A floating point 
name = 'Patrick' 			# A string

print beers_yesterday
print liters_beers_yesterday
print name




## Part II
str = 'Hello World! Today is Monday 03.08.2015!' 
print str # Prints complete string 
print str[0] # Prints first character of the string 
print str[2:5] # Prints characters starting from 3rd to 5th 
print str[2:] # Prints string starting from 3rd character 
print str * 2 # Prints string two times 
print str + 'TEST' # Prints concatenated string


## Part III

list = [ 'abcd', 786 , 2.23, 'wurst', 70.2 ] 
print list # Prints complete list 
print list[0] # Prints first element of the list 
print list[1:3] # Prints elements starting from 2nd till 3rd 
list[0] = 'beer' # Changes 'abcd’ to ’beer’ 
print list

## Part IV
image= [[0 ,2 ,1 ], [2, 300, 2], [2,2,2]]

print image[1][1]