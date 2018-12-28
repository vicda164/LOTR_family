import re
import filemanager
import wiki

re_spouse = re.compile("Spouse\W*([a-zA-Zí]*)")
re_children = re.compile("Children\W*([, a-zA-Zí]*)")
re_sibling = re.compile("Siblings\W*([a-zA-Zí]*)")
def str_to_dict(str_data):
    result = {}
    spouse = re_spouse.search(str_data)
    children = re_children.search(str_data)
    sibling = re_sibling.search(str_data)
    if spouse != None:
        result["spouse"] = spouse.group(1)
    if children != None:        
        c = [c.strip() for c in children.group(1).split(",") if c != " "]    
        result["children"] = c
    if sibling != None:
        s = [s.strip() for s in sibling.group(1).split(",") if s != " "]   
        result["sibling"] = s

    print("result:", result)
    return result

if __name__ == '__main__':
    infobox_data = wiki.fecthWikiPage("Elrond", section=0)
    str_data = filemanager.cleanhtml(infobox_data["parse"]["text"]["*"])
    silver_data = str_to_dict(str_data)        
    print(silver_data)
    #TODO save to file
