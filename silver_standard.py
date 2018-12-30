import re
import filemanager
import wiki
import os
import family_structure

re_spouse = re.compile("Spouse\W*([ a-zA-Zí]*)")
re_children = re.compile("Children\W*([, a-zA-Zí]*)")
re_sibling = re.compile("Siblings\W*([, a-zA-Zí]*)")
def str_to_dict(name, str_data):
    result = []
    spouse = re_spouse.search(str_data)
    children = re_children.search(str_data)
    sibling = re_sibling.search(str_data)
    if spouse != None:
        s = spouse.group(1)
        result.append((str(name), str(s), {"relation": "spouse"}))
    if children != None:        
        c = [c.strip() for c in children.group(1).split(",") if c != ""]   
        for child in c:
            result.append((str(name), str(child), {"relation": "child"}))         
    if sibling != None:
        s = [s.strip() for s in sibling.group(1).split(",") if s != ""]   
        for sibling in s:
            result.append((str(name), str(sibling), {"relation":"sibling"}))
        

    #print("result:", result)
    return result

def get_silver(name):
    infobox_data = filemanager.getCharacterInfobox(name) #wiki.fecthWikiPage(name, section=0)
    #if infobox_data != None:
    #str_data = filemanager.cleanhtml(infobox_data["parse"]["text"]["*"])
    print("get_silver")
    print(infobox_data)
    if infobox_data is None or infobox_data == [] or infobox_data == "":
        return None

    format_data = []
    for row in infobox_data:
        format_data.append((row[0], row[1],(row[2])))
    #silver_data = str_to_dict(name, infobox_data)
    #return silver_data
    #return None
    return format_data


if __name__ == '__main__':
    
    #names = filemanager.lotr_char_names()
    #for name in names:
    silver_data = get_silver("Arwen")
    print(silver_data)
        #if silver_data != {}:
        #    family_structure.add_relations(silver_data, file='./data/silver/')
        
