'''
Author: Kazark
Purpose: String Functions for DirSpync.
For further info see dirspync-io.py
'''

def minusstr(str1:str, str2:str) -> str:
    return str1 if str2 == '' else str1[:str1.index(str2)]
    
def fill(s:str, ch:str, leng:int) -> str:
    return "{0:{1}<{2}}".format(s, ch, leng)
    
def ellipsize(s:str, leng:int) -> str:
    return s[:leng-3] + '...' if len(s) > leng else s    
