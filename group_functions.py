# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 23:22:49 2019

@author: malte
"""
import dialogs

import os
import pickle
import glob

##########

#Globals

##########


cwd = os.getcwd()
persons = []
project_file_ending = "lst"
loaded_groupnames = []
month_list = []

class person():
    per_id = 0
    name = ""
    active = False
    
    def __init__(self, newname , state):
        self.per_id = len(persons)+1
        self.name = newname
        if state:    
            self.active = True
        else:
            self.active = False  
        persons.append(self)

##########

#Functions

##########

def list_folder():
    """ 
    Listet nur Verzeichnisse in diesem Verzeichnis ('.') auf
    """
    reslist = []
    for root, dirs, files in os.walk(cwd):
        for name in dirs:
            reslist.append(name)
    return reslist


def create_group():

    global project_name
    ask_for_members="y"
    groupname = dialogs.get_input("Gruppenname: ")
    while(True):
        if (ask_for_members=="y"):
            print("Neue Person")
            new_member_name = dialogs.get_input("Name: ")
            person(new_member_name,True)
    
            print("weitere Person hinzufuegen?")
            ask_for_members = dialogs.get_input("y/n \n")
        else:
            break
    os.mkdir(groupname)
    fileobj = open(os.path.join(groupname, groupname + "_persons.lst") ,"wb")
    pickle.dump([groupname , persons] , fileobj)
    fileobj.close()



def find_groups():        
#suche projektdateien

    dir_list = list_folder()
    found_project = []
    
    for dirname in dir_list:
        directory = os.path.join(cwd,dirname)
        files_in_cwd = os.listdir(directory)

        for filename in files_in_cwd:
            if filename[-len(project_file_ending):] == str(project_file_ending):
            
                found_project.append(dirname)
                
    return found_project

def load_group_interaction(loaded_groupnames):
        #global working_groupname
        global month_list
        global cwd
        
        print("Found:")
        options = []
        for name in loaded_groupnames:
            options.append(name)
            print(name)
        
        group = dialogs.get_input("Load group: [groupname]: ")
        print("\n")
        if group in loaded_groupnames:
            #load group
            load_group(group)
            working_groupname = group
        else:
            print("Input Error")
            return ""
            
        month_list = []
        os.chdir(os.path.join(cwd,working_groupname))
        for file in glob.glob("*.mon"):
            month_list.append(file)
            
        return group

def load_group(groupname):
    global persons
    global groupinfo

    filename = groupname+"_persons."+project_file_ending
    loadfile = open(os.path.join(cwd,groupname,filename),'rb')
    groupinfo = pickle.load(loadfile)
    persons = groupinfo[1]
    groupinfo = groupinfo[0]
    loadfile.close()


def edit_activations(groupname):
    print()    
    
    do = True
    option_list = []    
    while(do):
        for person in persons:
            if person.active:
                active = "active"
            else:
                active = "deactivated"
            option_list.append(person.per_id)
            print("id: " + str(person.per_id) + " - " + person.name + " " + active)
    
        selection=dialogs.get_number("Please Select id:") 
        if selection not in option_list:
            print("input error")
        else:
            selection_index = option_list.index(selection)
            persons[selection_index].active = not persons[selection_index].active
            fileobj = open(os.path.join(groupname + "_persons.lst") ,"wb")
            pickle.dump([groupname , persons] , fileobj)
            fileobj.close()
        
        check = dialogs.get_yesno("Edit more? [y/n]")
        if check == "n":
            do = False
    return True

def edit_group(groupname):
    editing_options = ["add member","de/activate member"]
    menu = {}
    
    for idx,item in enumerate(editing_options):
        menu[idx]=item
        
    options=menu.keys()
    for entry in options: 
            print (entry, menu[entry])
            
    selection=dialogs.get_number("Please Select:") 
    try:
        menu[selection]
    except KeyError:
        print("input error")
        return edit_group(groupname)

    if menu[selection] == "add member": 
        print("not able to add members yet")
    elif menu[selection] == "de/activate member": 
        edit_activations(groupname)
    return True