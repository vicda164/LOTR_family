import os

import plac
import numpy as np

import filemanager
import relation_extraction
import graph
import silver_standard as silver

def find_family_relations(to_read=[], read_bios=[], relations=[]):
    """
        Recursivly read documents of characters that occur in a text from the root name.
        For each name extract relations.
    """
    if len(to_read) == 0:
        # create validation data
        #for name in to_read:
        #    filemanager.getCharacterInfobox(name)
        return relations

    name = to_read[0]
    print(name, to_read, read_bios)
    rel = None
    char_bio = filemanager.getCharacterDescription(name)
    read_bios.append(name)
    to_read.remove(name)

    if char_bio != None:
        rel = relation_extraction.extract_relations(char_bio)
    
        if rel is None or rel == []:
            if len(to_read) > 0:
                return find_family_relations(to_read=to_read, read_bios=read_bios, relations=relations) 
            else:  
                return relations
    else:
        return find_family_relations(to_read=to_read, read_bios=read_bios, relations=relations) 
    
    relations += rel    
    print(rel)
    relatives = np.array(rel)[:,1] # get column 1
    relatives = [r for r in relatives if r not in read_bios]
    to_read += relatives
    
    return find_family_relations(to_read=to_read, read_bios=read_bios, relations=relations)
    

def create_validation_data(to_read=[], read_bios=[], relations=[]):
    """ 
        Recursivly read infoboxes of characters mentioned from the root name.        
    """

    print(to_read, read_bios, relations)
    if len(to_read) == 0:
        return relations

    name = to_read[0]
    rel = silver.get_silver(name)    
    read_bios.append(name)
    to_read.remove(name)

    if rel is None or rel == []:
        if len(to_read) > 0:
            return create_validation_data(to_read=to_read, read_bios=read_bios, relations=relations) 
        else:
            return relations

    relations += rel
    print("rel:", rel)
    relatives = np.array(rel)[:,1]
    relatives = [r for r in relatives if r not in read_bios]
    to_read += relatives

    return create_validation_data(to_read=to_read, read_bios=read_bios, relations=relations) 

def get_silver_family(name):
    wanted_file = "./data/silver/" + name 
    validation_data = []

    if name in os.listdir("./data/silver/"):
        print("EXISTS")
        validation_data = graph.get(wanted_file)
    else:
        #if not os.path.exists(wanted_file):
        #    with open(wanted_file, 'w'): pass            
        validation_data = create_validation_data([name])
        print("Val_data:", validation_data)
        if validation_data != []:        
            graph.add_relations(validation_data, file=wanted_file)
        
    return validation_data

def _validate(family_set, silver_set):
    #TODO compare guess and silver
    """
        recall = (relevant + retrived) / relevant

        precision = (relevant + retrived) / retrived
    """

    print("_validate:")
    print("family:" ,family_set)
    print("silver:" ,silver_set)

    false_positive = []
    true_positive = []

    for relation in family_set:
        print(relation)
        rel = relation[2]["relation"]
        edge = (relation[0], relation[1], {"relation":rel})
        if edge in silver_set:
            true_positive.append(edge)
        else:
            false_positive.append(edge)

    if len(family_set) == 0:
        return (0,0,0) 
    recall = len(true_positive) / len(silver_set)
    precision = len(true_positive) / len(family_set)
    if recall + precision == 0:
        return (0,0,0)
    f1 = (2 * recall * precision) / (recall + precision)

    return (recall, precision, f1)

@plac.annotations(
    name=("Character name", "positional", None, str),
    disbale_cache=("Delete family tree from root name Name", "flag", "r"),
    validate=("Validate", "flag", "v"),
    draw=("Draw graph", "flag", "d"))
def run(name, disbale_cache, validate, draw):  
    if disbale_cache or name not in os.listdir("./data/family/"):        
        if name in os.listdir("./data/family/"):
            os.remove("./data/family/" + name)            

        if name in os.listdir("./data/silver/"):
            os.remove("./data/silver/" + name)

        family_tree = find_family_relations(to_read=[name])
        family = graph.add_relations(family_tree, "./data/family/"+name)        
    else:     
        family = graph.get("./data/family/"+name)
    

    print("RUN 1")    
    if validate:
        silver = get_silver_family(name)
        (recall, precision, f1) = _validate(family, silver)

        print("recall:", recall)
        print("precisision:", precision)
        print("F1:", f1)


        if draw:
            file1 = "./data/family/" + name
            file2 = "./data/silver/" + name
            graph.draw(file1, file2) 
    else:
        if draw:
            file1 = "./data/family/" + name            
            graph.draw(file1) 
    
    print("MAIN DONE")


if __name__ == "__main__":
    plac.call(run)