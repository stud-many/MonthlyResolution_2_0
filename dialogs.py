# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 23:25:59 2019

@author: malte
"""

def get_yesno(show_string):
    out = ""

    out = input(show_string)
    while (out != "y" and out != "n"):
        print("Inputerror. Case sensitive [y/n]")
        return get_yesno(show_string)
    return out

def get_input(show_string):
    out = ""

    out = input(show_string)

    return out

def get_number(show_string):
    
    out= ""
    out = input(show_string)
    checkbool = True
    for c in out:
        if ord(c) < 48 or ord(c) > 57:
            checkbool = False
    
    while not checkbool:
        print("Inputerror. Integer needed")
        return get_number(show_string)
    return int(out)
    
def get_float(show_string):
    
    out= ""
    out = input(show_string)
    checkbool = True
    for c in out:
        if ord(c) < 48 or ord(c) > 57:
            if ord(c)!=46:
                checkbool = False
    
    while not checkbool:
        print("Inputerror. Float in format [x.x] needed")
        return get_number(show_string)
    return float(out)

def get_date():
    showstring = "Month in format [mm.yy] :"
    numbers = ["0","1","2","3","4","5","6","7","8","9"]
    date = input(showstring)
    date = date.split(".")

    if len(date) != 2:
        print ("Input Error. Use a dot in [mm.yy]")
        return get_date()

    countnumbers_month = 0
    countnumbers_year = 0
    
    for char in date[0]:
        if char in numbers:
            countnumbers_month += 1
    for char in date[1]:
        if char in numbers:
            countnumbers_year += 1

    if (countnumbers_month != 2 or countnumbers_year != 2):
        print("Input Error. Month and year in format [mm.yy]")
        return get_date()        
    
    month = int(date[0])
    year = int(date[1])
    while (month<1 or month > 12) or (year<0 or year>99):
        print("Input Error. Date does'nt make any sense. Use format [mm.yy]")
        return get_date()
    else:
        year = str(year)
        month = str(month)
        if len(month) == 1:
            month = "0"+month
            
        return [month,year]

