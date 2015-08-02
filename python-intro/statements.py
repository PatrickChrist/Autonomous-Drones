# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 23:10:10 2015

@author: patrickchrist
"""

## Part I

a=input('Input a value for a:')
if (a > 0): 
    print 'positiv' 
elif (a == 0): 
    print 'null'
else: 
    print 'negativ'

## Part II

sixpack = ['Augustiner', 'Tegernseer', 'Tegernseer']
for beer in sixpack:
    print 'I drink', beer 

## Part III

beer_count = 0 
while (beer_count < 9):
    print 'The beer count is:', beer_count 
    beer_count = beer_count + 1
