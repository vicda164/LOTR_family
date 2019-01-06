import os

import plac
import numpy as np

import filemanager
import relation_extraction
import graph
import silver_standard as silver
import train

def find_family_relations(to_read=[], read_bios=[], relations=[]):
    """
        Recursivly read documents of characters that occur in a text from the root name.
        For each name extract relations.
    """
    if len(to_read) == 0:
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
    
    # Don't add duplicates, thought add same relation again if found in different text.    
    relations += [r for r in rel if r not in relations]    
    # Get both first and second column, and no duplicates
    relatives = np.unique( np.array(rel)[:,[0,1]].flatten())
    relatives = [r for r in relatives if r not in read_bios]
    to_read += relatives
    
    return find_family_relations(to_read=to_read, read_bios=read_bios, relations=relations)
    

def create_validation_data(to_read=[], read_bios=[], relations=[]):
    """ 
        Recursivly read infoboxes of characters mentioned from the root name.        
    """

    #print(to_read, read_bios, relations)
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

    # Don't add duplicates    
    relations += [r for r in rel if r not in relations] 
    # Get both first and second column, and no duplicates
    relatives = np.unique( np.array(rel)[:,[0,1]].flatten())
    relatives = [r for r in relatives if r not in read_bios]
    to_read += relatives

    return create_validation_data(to_read=to_read, read_bios=read_bios, relations=relations) 

def get_silver_family(name):
    wanted_file = "./data/silver/" + name 
    validation_data = []

    if name in os.listdir("./data/silver/"):
        #print("EXISTS")
        validation_data = graph.get(wanted_file)
    else:
        #if not os.path.exists(wanted_file):
        #    with open(wanted_file, 'w'): pass            
        validation_data = create_validation_data([name])
        #print("Val_data:", validation_data)
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
        #print(relation)
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

    print("Length of validation set:", len(silver_set))
    print("Length of family set:", len(family_set))

    return (recall, precision, f1)

@plac.annotations(
    name=("Character name", "positional", None, str),
    #model=("Model to use", "option", "m")
    disbale_cache=("Delete family tree from root name Name", "flag", "r"),
    validate=("Validate", "flag", "v"),
    s=("Just get silver nothing else", "flag", "s"),
    draw=("Draw graph", "flag", "d"),
    fetchall=("Fetch all character desciptions of names in kaggle_data/Characters","flag","f"))
def run(name, disbale_cache, validate, s, draw,fetchall):
    if fetchall:
        print("Fetch all descriptions")
        names = filemanager.lotr_char_names()
        for name in names:
            filemanager.getCharacterDescription(name)
        print("DONE")
        
        #print("Train")
        #status = train.train(training_set)
        #if status == "OK":
        #    print("DONE")
        #    print("Successfully finished")
        #else:
        #    print("Error while training")
        return

    if s:
        if name in os.listdir("./data/silver/"):
            os.remove("./data/silver/" + name)
        silver = get_silver_family(name)
        print(silver)
        return

    
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
        #TODO BUG? get_silver_family is inconsistant
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
    if "data" not in os.listdir():
        os.makedirs("./data/character_bio")
        os.makedirs("./data/character_infobox")
        os.makedirs("./data/family")
        os.makedirs("./data/silver")
    if "model" not in os.listdir():
        os.makedirs("./model")
    plac.call(run)



#TODO TEST if get_silver is correct:
# Test DATA for Elrond
"""
several daughters,Arwen,{'relation': 'parent'}
Elladan,Elrond,{'relation': 'parent'}
Vardamir Nólimon,Elros,{'relation': 'parent'}
Vardamir Nólimon,Unnamed wife,{'relation': 'spouse'}
Elrond,Elros,{'relation': 'sibling'}
Elrond,Celebrían,{'relation': 'spouse'}
Elros,Atanalcar,{'relation': 'parent'}
Eldarion,Arwen,{'relation': 'parent'}
Eldarion,Aragorn II Elessar,{'relation': 'parent'}
Eldarion,Several unnamed sisters,{'relation': 'sibling'}
Possible unnamed wife,Manwendil,{'relation': 'spouse'}
Possible unnamed wife,Atanalcar,{'relation': 'spouse'}
Elrohir,Arwen,{'relation': 'sibling'}
Elrohir,Elrond,{'relation': 'parent'}
Manwendil,Elros,{'relation': 'parent'}
Arwen,Elladan,{'relation': 'sibling'}
Arwen,Aragorn II Elessar,{'relation': 'spouse'}
Arwen,Elrond,{'relation': 'parent'}
Tindómiel,Elros,{'relation': 'parent'}
Tindómiel,Unknown,{'relation': 'spouse'}
Aragorn II Elessar,at least two daughters,{'relation': 'parent'}
"""