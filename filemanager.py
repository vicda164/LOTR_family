import sys
import os
import re
import csv

import numpy as np

import wiki
import silver_standard
import graph

DATA_FOLDER = "data/character_bio/"

def cleanhtml(raw_html, delimiter=", "):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, delimiter, raw_html)
    return cleantext


def readCSV(filename):
    # returns list object of csv
    rows = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for i,row in enumerate(reader):
            if i != 0:
                rows.append(row)
    
    return rows

def writeCSV(filename, content):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(content)


def lotr_char_names():
    #get list of csv rows
    #extract Names    
    rows = readCSV("kaggle_data/Characters.csv")
    rows = np.array(rows)
    print(rows.shape) 
    names = rows[:,0] # get first column        
    return names


def getFromWiki(name):
    # fetch character html-page
    html = wiki.fecthWikiPage(name)
    return html

def _getDescriptionAndBio(name):
    """
        returns text from both biography section and the text
        from first introduction section(but removes infobox)
    """
    p_reg = re.compile("<p>\n*(.*)\n*</p>")
    biography_dirty = wiki.fecthWikiPage(name, section=1)
    if not biography_dirty:
        print("WARNING: no biography section found for ", name)
        return None
    
    biography_dirty = biography_dirty["parse"]["text"]["*"]
    biography = cleanhtml(biography_dirty, delimiter="")

    description_dirty = wiki.fecthWikiPage(name, section=0)
    if not description_dirty:
        print("WARNING: no description section found for ", name)
        return None

    description_dirty = description_dirty["parse"]["text"]["*"]      
    description = p_reg.findall(description_dirty)    
    description = " ".join(description)
    description = cleanhtml(description, delimiter="")    
    description += biography    
    return description

def getFromText(name):
    """
    Return biography as text
    """
    if ".txt" in name:
        filename = name
    else:
        filename = DATA_FOLDER + name + ".txt"
        
    try:
        with open(filename, "r") as file:
            return file.read()
    except Exception as identifier:
        return "ERROR: " + str(identifier)
    


def saveToText(filename, text):
    """
    Saves biography as text to .txt file.
    """
    filename = DATA_FOLDER + filename + ".txt"
    try:
        with open(filename, "w") as file:
            file.write(text)
            return 0 #OK
    except Exception as identifier:
        return "ERROR: " + str(identifier)

    

def getCharacterDescription(name):
    """
    If exists localy then get it else fecth from wiki and save to local. Clean before return.
    """
    print("getCharacterDescription", name)
    biography = ""
    char_bios_dir = os.listdir(DATA_FOLDER)
    wanted_file = name + ".txt"
    if wanted_file in char_bios_dir:
    #check if stored 
        biography = getFromText(name)        
    # else
    else:
        try:
            biography = _getDescriptionAndBio(name)
            if biography is not None:                 
                saveToText(name, biography)
            else:
                return None
        except Exception as identifier:
            print("Error: " , str(identifier))

    return biography
    
def getCharacterInfobox(name):
    """
    If exists localy then get it else fecth from wiki and save to local. Clean before return.
    """
    print("getCharacterInfobox", name)
    infobox = None
    data_foler = "./data/character_infobox/"
    dir = os.listdir(data_foler)    
    if name in dir:
    #check if stored 
        print("PASS")
        #infobox = readCSV(data_foler + wanted_file)        
        infobox = graph.get(data_foler + name)
    # else
    else:
        try:
            html = wiki.fecthWikiPage(name, section=0)
            if html == "":
                return None            
            # clean, structure and save
            uncleantext = html["parse"]["text"]["*"]        
            text = cleanhtml(uncleantext, delimiter=", ")               
            infobox = silver_standard.str_to_dict(name, text)            
            save_to = "./data/character_infobox/" + name
            graph.add_relations(infobox, save_to)# writeCSV(save_to, infobox)
            #graph.add_relations(silver, file=save_to)                 
        except Exception as identifier:
            print("Error: " , str(identifier))

    return infobox
         
if __name__ == '__main__':
    #os.makedirs("./data/character_infobox/")   
    """ 
    args = sys.argv[1:]
    print(args)
    if len(args) < 1:
        print("Error: arg0 = charName")
        #return 1
    
    name = args[0]

    char_description = getCharacterDescription(name)
    print("RESULT")
    print(char_description)
    #return char_description


    infobox = getCharacterInfobox(name)
    print("RESULT")
    print(infobox)
    """    
    print(_getDescriptionAndBio("Elrond"))