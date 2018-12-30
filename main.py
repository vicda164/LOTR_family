import os

import plac
import numpy as np

import filemanager
import relation_extraction
import family_structure
import silver_standard as silver

def find_family_relations(name, to_read=[], read_bios=[], relations=[]):
    """
        Recursivly read documents of characters that occur in a text from the root name.
        For each name extract relations.
    """

    print(name, to_read, read_bios, relations)
    if len(to_read) == 0:
        # create validation data
        for name in to_read:
            filemanager.getCharacterInfobox(name)
        return relations

    rel = None
    char_bio = filemanager.getCharacterDescription(name)
    if char_bio != None:
        rel = relation_extraction.extract_relations(char_bio)
    read_bios.append(name)
    to_read.remove(name)

    if rel is None or rel == []:
        if len(to_read) > 0:
            return find_family_relations(to_read[0], to_read=to_read, read_bios=read_bios, relations=relations) 
        else:  
            return relations
    
    relations += rel    
    print(rel)
    relatives = np.array(rel)[:,1] # get column 1
    relatives = [r for r in relatives if r not in read_bios]
    to_read += relatives

    return find_family_relations(to_read[0], to_read=to_read, read_bios=read_bios, relations=relations)


def create_validation_data(name, to_read=[], read_bios=[], relations=[]):
    """ 
        Recursivly read infoboxes of characters mentioned from the root name.        
    """

    print(name, to_read, read_bios, relations)
    if len(to_read) == 0:
        return relations

    rel = silver.get_silver(name)    
    read_bios.append(name)
    to_read.remove(name)

    if rel is None or rel == []:
        if len(to_read) > 0:
            return create_validation_data(to_read[0], to_read=to_read, read_bios=read_bios, relations=relations) 
        else:  
            return relations

    relations += rel
    print("rel:", rel)
    relatives = np.array(rel)[:,1]
    relatives = [r for r in relatives if r not in read_bios]
    to_read += relatives

    return create_validation_data(to_read[0], to_read=to_read, read_bios=read_bios, relations=relations) 

def get_silver_family(name):
    wanted_file = "./data/silver/" + name 
    validation_data = []

    if name in os.listdir("./data/silver/"):
        print("EXISTS")
        validation_data = family_structure.get_family_tree(wanted_file)
    else:
        #if not os.path.exists(wanted_file):
        #    with open(wanted_file, 'w'): pass            
        validation_data = create_validation_data(name, [name])
        print("Val_data:", validation_data)
        silver = family_structure.add_relations(validation_data, file=wanted_file)
        
    return validation_data

def _validate(family, silver):
    #TODO compare guess and silver
    return None

@plac.annotations(
    name=("Character name", "positional", None, str),
    validate=("Validate", "flag", "v"),
    draw=("Draw graph", "flag", "d"))
def run(name, validate, draw):  
    
    family_tree = find_family_relations(name, to_read=[name])
    family = family_structure.add_relations(family_tree, "./data/family/"+name)
    #family_structure.draw_graph()
    

    #for rel in family_tree:
    #    print(rel)   

    
    if validate:
        silver = get_silver_family(name)
        _validate(family_tree, silver)

        if draw:
            file1 = "./data/family/" + name
            file2 = "./data/silver/" + name
            family_structure.draw_graph(file1, file2) 
    else:
        if draw:
            file1 = "./data/family/" + name            
            family_structure.draw_graph(file1) 

if __name__ == "__main__":
    plac.call(run)