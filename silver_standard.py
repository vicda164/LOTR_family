import re
import filemanager
import wiki
import os

import graph

re_spouse = re.compile("Spouse\W*([ a-zA-Zíáóé]*)")
re_children = re.compile("Children\W*([, a-zA-Zíáóé]*)")
re_sibling = re.compile("Siblings\W*([, a-zA-Zíáóé]*)")
#re_parent = re.compile("Parentage\W*([, a-zA-Zí]*)")
def str_to_dict(name, str_data):
    str_data = str_data.replace("and", ", ")    
    result = []
    spouse = re_spouse.search(str_data)
    children = re_children.search(str_data)
    sibling = re_sibling.search(str_data)
    #parent = re_parent.search(str_data)
    if spouse != None:
        s = spouse.group(1)
        result.append((str(name), str(s), {"relation": "spouse"}))
    if children != None:                    
        c = [c.strip() for c in children.group(1).split(",") if c.split()]
        for child in c:
            result.append((str(name), str(child), {"relation": "parent"}))         
    if sibling != None:        
        s = [s.strip() for s in sibling.group(1).split(",") if s.split()]          
        for sibling in s:            
            result.append((str(name), str(sibling), {"relation":"sibling"}))
    #if parent != None:
    #    s = [s.strip() for s in parent.group(1).split(",") if not s]   
    #    for parent in s:
    #        result.append((str(name), str(parent), {"relation":"parent"}))

    #print("result:", result)
    return result

def get_silver(name):
    infobox_data = filemanager.getCharacterInfobox(name)
    print("get_silver")
    print(infobox_data)
    if infobox_data is None or infobox_data == [] or infobox_data == "":
        return None

    format_data = []
    filter = ["Unnamed", "Unnamed wife", "Unknown", "None"]
    for row in infobox_data:
        if row[0] or row[1] or row[0] in filter or row[1] in filter:
            # if either names are empty then skip
            format_data.append((row[0], row[1], (row[2])))    
    return format_data


if __name__ == '__main__':
    """
    names = filemanager.lotr_char_names()
    for name in names:
        silver_data = get_silver(name)    
        if silver_data != {}:
            graph.add_relations(silver_data, file='./data/test')
    """
    os.remove("./data/character_infobox/Elrond")
    print(get_silver("Elrond"))
        
