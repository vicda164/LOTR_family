import sys
import os
import re
import csv

import wiki


DATA_FOLDER = "data/character_bio/"

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, ', ', raw_html)
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


def getFromWiki(name):
    # fetch character html-page
    html = wiki.fecthWikiPage(name)
    return html

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
            html = getFromWiki(name)
            # clean
            description = html["parse"]["text"]["*"]
            biography = cleanhtml(description)   
            saveToText(name, biography)        
        except Exception as identifier:
            print("Error: " , str(identifier))

    return biography
    
        
         
if __name__ == '__main__':
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