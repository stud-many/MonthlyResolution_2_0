# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 02:00:35 2019

@author: malte
"""

from datetime import date

import dialogs
import group_functions

import os
import pickle
import glob
import copy

##########

#Globals

##########


cwd = os.getcwd()
persons = []
project_file_ending = "lst"
loaded_groupnames = []


class month_timestat():
    year = 0
    month = 0
    days = 0
    
    def __init__(self, new_year , new_month):
            
            self.year = new_year
            self.month = new_month
            
            if self.month < 12:
                self.days = (date(self.year,self.month+1,1)-date(self.year,self.month,1)).days 
            else:
                self.days =(date(self.year+1,1,1)-date(self.year,self.month,1)).days
        
class outlay():
    per_id = 0
    amount = 0
    days = 0
    extra_days = 0
    
    def __init__(self, new_id , new_amount,new_days,new_extra):
        self.per_id = new_id
        self.amount = new_amount
        self.days = new_days
        self.extra_days = new_extra


class month_costs():
    days_of_presents = 0
    payments = []
    costs = 0
    daily = 0
    
    def __init__(self, payments):
        self.payments = payments
        for entry in payments:
            self.costs += entry.amount
            self.days_of_presents += entry.days
            self.days_of_presents += entry.extra_days
    
        self.daily = self.costs / self.days_of_presents

def list_folder():
    """ 
    Listet nur Verzeichnisse in diesem Verzeichnis ('.') auf
    """
    reslist = []
    for root, dirs, files in os.walk(cwd):
        for name in dirs:
            reslist.append(name)
    return reslist

def list_specific_folder(dirpath):
    """ 
    Listet nur Files in übermitteltem Verzeichnispath auf
    """
    reslist = []
    for root, dirs, files in os.walk(dirpath):
        for name in files:
            reslist.append(name)
    return reslist


def month_active_id_list():
    listing = []
    persons = group_functions.persons
    for per in persons:
        if per.active:
            listing.append(per.per_id)
    return listing

def name_by_id(per_id):
    persons = group_functions.persons
    for per in persons:
        if per.per_id == per_id:
            return per.name

def find_transaction(working_stats):
    biggest_positive = 0 #gehörts diesem?
    biggest_positive_owner = 0
    biggest_negative = 0 #schuldet dieser?
    biggest_negative_owner = 0
    
    for item in working_stats:
        if item[3] > biggest_positive:
            biggest_positive_owner = item[0]
            biggest_positive = item[3]
        elif item[3] < biggest_negative:
            biggest_negative_owner = item[0]
            biggest_negative = item[3]
    trans = 0
    if biggest_positive >= abs(biggest_negative) :
        trans = abs(biggest_negative)
    elif abs(biggest_negative) > biggest_positive:
            trans = biggest_positive
    return [biggest_positive_owner,biggest_negative_owner,trans]
            
class month():
  
    def __init__(self, year , month):
        self.outlays = []
        self.costs = object
        self.personal_stats = [] #id,soll,ist
#        self.transaction_list = []    #MUSS AUS DIESER KLASSE ENTFERNT UND IN ABRECHNUNGSKLASSE GEPACKT WERDEN
    #initiiere monat
        del self.personal_stats[:]
        
        self.year = year
        self.month = month
            
        self.month_timestats = month_timestat(self.year,self.month)
        
        self.active_id_list = month_active_id_list()
        self.processed = False #NEUER BOOL. MUSS VERÄNDERT WERDEN AUF TRUE WENN ABGERECHNET WURDE
    
    #initiiere zahlungen
    
        for per_id in self.active_id_list:
            print(name_by_id(per_id))
            new_outlay_amount = dialogs.get_float("Zahlung: ")
            new_outlay_days = dialogs.get_number("Tage: ")
            new_outlay_extra = dialogs.get_number("Extra Tage: ")
            self.outlays.append(outlay(per_id, new_outlay_amount, new_outlay_days, new_outlay_extra))
    
    #initiiere kosten
        self.costs = month_costs(self.outlays)
    
        for identifier in self.active_id_list:
            soll = 0
            ist = 0
            days = 0
            for outl in self.outlays:
                if outl.per_id == identifier:
                    days = outl.days+outl.extra_days
                    soll = round(days*self.costs.daily,2)
                    ist = outl.amount
                    diff = round(ist - soll,2)
            self.personal_stats.append([identifier,soll,ist,diff])

def find_unprocessed_month(groupname):
    unprocessed = []
    month_files = []
    for file in list_specific_folder(os.path.join(cwd,groupname)):
        if file[-3:] == "mon":
            month_files.append(file)
    
    for file in month_files:
        fobj = open(os.path.join(cwd,groupname,file) ,"rb")
        month_info = pickle.load(fobj)[0]
        fobj.close()
        if month_info.processed == False:
            unprocessed.append(file)
    return unprocessed

class resolution():
    def __init__(self, groupname):
        self.groupname = groupname
        self.unprocessed_month = find_unprocessed_month(groupname)
        self.transaction_list = []
        
        self.personal_stats_read = []
        self.personal_stats_sum = []
        
        for month in self.unprocessed_month:
            fobj = open(os.path.join(cwd,groupname,month) ,"rb")
            month_info = pickle.load(fobj)[0]
            fobj.close()
            self.personal_stats_read.append(month_info.personal_stats)
        
        stats_copy = copy.deepcopy(self.personal_stats_read) #verbesserungswürdig
        for stats in stats_copy:
            for stat_entry in stats:
                
                memberid = stat_entry[0]
                if memberid not in [i[0] for i in self.personal_stats_sum]:
                    self.personal_stats_sum.append(stat_entry)

                else:
                    #Finde richtigen Index von personal_stats_sum für Summierung
                    stats_index = [i[0] for i in self.personal_stats_sum].index(memberid)
                    for idx,item in enumerate(stat_entry):
                        if idx>0:
                            self.personal_stats_sum[stats_index][idx] += item
                        
    #berechne transaktionen

        self.working_stats = copy.deepcopy(self.personal_stats_sum)
    
        while True:

            trans = find_transaction(self.working_stats)
            #print(trans)
            if round(trans[2],2) > 0:
                trans[2] = round(trans[2],2)
                self.transaction_list.append(trans)
                for idx, item in enumerate(self.working_stats):
                    if item[0] == trans[0]: #posjtive buchung
                        self.working_stats[idx][2] += trans[2]
                        self.working_stats[idx][3] -= trans[2]
                    elif item[0] == trans[1]:
                        self.working_stats[idx][2] -= trans[2]
                        self.working_stats[idx][3] += trans[2]
            else:
                #runde ergebnisse
                for item in self.working_stats:
                    item[2] = round(item[2],2)
                    item[3] = round(item[3],2)
                break

        #report
        for item in self.transaction_list:
            print(name_by_id(item[0])+" erhaelt "+ str(item[2]) + " von " + name_by_id(item[1]))  
           
        for filename in self.unprocessed_month:
            with open(os.path.join(cwd,groupname,filename), "rb") as pfile:
                info = pickle.load(pfile)
            info[0].processed = True
            with open(os.path.join(cwd,groupname,filename), "wb") as pfile:
                pickle.dump(info,pfile)
