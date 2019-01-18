import os

import plac
import numpy as np

import filemanager
import relation_extraction
import graph
import silver_standard as silver
import train

def find_family_relations(model, to_read=[], read_bios=[], relations=[]):
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
        rel = relation_extraction.extract_relations(char_bio, model=model)

        if rel is None or rel == []:
            if len(to_read) > 0:
                return find_family_relations(model=model, to_read=to_read, read_bios=read_bios, relations=relations) 
            else:  
                return relations
    else:
        return find_family_relations(model=model, to_read=to_read, read_bios=read_bios, relations=relations) 
    
    # Don't add duplicates, thought add same relation again if found in different text.    
    relations += [r for r in rel if r not in relations]    
    # Get both first and second column, and no duplicates
    relatives = np.unique( np.array(rel)[:,[0,1]].flatten())
    print(relatives)
    relatives = [r for r in relatives if r not in read_bios and r not in to_read]
    to_read += relatives

    return find_family_relations(model=model, to_read=to_read, read_bios=read_bios, relations=relations)
    

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
        print("EXISTS")
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
    #print("family:" ,family_set)
    #print("silver:" ,silver_set)

    false_positive = []
    true_positive = []
    false_relation_but_correct_pair = []
    family = []
    #family_names = np.array(silver)[:,[1,2]].flatten()
    for relation in family_set:
        #print(relation)
        rel = relation[2]["relation"]
        edge = (relation[0], relation[1], {"relation":rel})
        family.append(edge)
        if edge in silver_set:# and edge[0] in family_names:
            true_positive.append(edge)            
            #elif and edge[0] in family_names:
        else:
            false_positive.append(edge)        

    count = 0
    # TODO: validate if correct. do tests
    for relation in false_positive:
        count += 1
        for s in silver_set:            
            if relation[0:2] == s[0:2]:
                false_relation_but_correct_pair.append(relation)
                print(relation, s)
                break
    #print("fp:", len(false_relation_but_correct_pair))
    print(count)


    if len(family_set) == 0:
        return (0,0,0,0,0,0)
    recall = len(true_positive) / len(silver_set)
    precision = len(true_positive) / len(family_set)
    if recall + precision == 0:
        return (0,0,0,0,0,0)
    f1 = (2 * recall * precision) / (recall + precision)

    silver_minus_intersect = [i for i in silver_set if i not in true_positive]
    family_minus_intersect = [i for i in family if i not in true_positive]
    print("####")
    print(len(silver_minus_intersect), len(family_minus_intersect), len(false_relation_but_correct_pair))
    recall_pair = len(false_relation_but_correct_pair) / len(silver_minus_intersect)
    precision_pair = len(false_relation_but_correct_pair) / len(family_minus_intersect)
    if recall_pair + precision_pair == 0:
        return (recall, precision, f1,0,0,0)

    f1_pair = (2 * recall_pair * precision_pair) / (recall_pair + precision_pair)
    print("Length of validation set:", len(silver_set))
    print("Length of family set:", len(family_set))

    return (recall, precision, f1, recall_pair, precision_pair, f1_pair)

def latex_tabell(name, family_no_model, family, silver):
    # TODO add measure of # correct edges      
    (recall0, precision0, f10, rp0, pp0, fp0) = _validate(family_no_model, silver)
    (recall, precision, f1, rp, pp, fp) = _validate(family, silver)
    print("\multicolumn{{1}}{{c}}{} & \\\ \cline{{1-3}}".format(name))
    print("Measure     & Before training & After Training \\\ \hline")
    print("Recall      & {:.2f}({:.2f})     & {:.2f}({:.2f})    \\\ ".format(recall0, recall0 + rp0, recall, recall+rp))
    print("Precision   & {:.2f}({:.2f})     & {:.2f}({:.2f})     \\\ ".format(precision0, precision0+pp0, precision, precision+pp))
    print("F1-score    & {:.2f}({:.2f})     & {:.2f}({:.2f})     \\\ ".format(f10,f10+ fp0, f1, f1+fp))
    print("Relations   & {}({})     & {}({})      \\\ \hline".format(len(family_no_model), len(silver), len(family), len(silver)))
    #print("".format())

@plac.annotations(
    name=("Character name", "positional", None, str),
    #model=("Model to use", "option", "m")
    disbale_cache=("Delete family tree from root name Name", "flag", "r"),
    validate=("Validate", "flag", "v"),
    svalidate=("Scientific validation, validate against untrained model and silver data", "flag", "V"),
    s=("Just get silver nothing else", "flag", "s"),
    draw=("Draw graph", "flag", "d"),
    fetchall=("Fetch all character desciptions of names in kaggle_data/Characters","flag","f"))
def run(name, disbale_cache, validate, svalidate, s, draw,fetchall):
    MODEL = "./model_slim"

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

        family_tree = find_family_relations(to_read=[name], model=MODEL)
        family = graph.add_relations(family_tree, "./data/family/"+name)        
    else:     
        family = graph.get("./data/family/"+name)
    

    print("RUN 1")    
    if validate:
        silver = get_silver_family(name)
        #(recall, precision, f1) = _validate(family, silver)

        #print("recall:", recall)
        #print("precisision:", precision)
        #print("F1:", f1)


        if draw:
            file1 = "./data/family/" + name
            file2 = "./data/silver/" + name
            graph.draw(file1, file2) 
    else:
        if draw:
            file1 = "./data/family/" + name            
            graph.draw(file1) 
    

    if svalidate:
        family = None
        family_no_model = None
        silver = get_silver_family(name)

        if name not in os.listdir("./data/family/"):
            family_tree = find_family_relations(to_read=[name], model=MODEL)
            family = graph.add_relations(family_tree, "./data/family/"+name)        
        else:
            family = graph.get("./data/family/"+name)

        if name not in os.listdir("./data/family_no_model/"):
            family_tree_no_model = find_family_relations(to_read=[name], model="en_core_web_sm")
            family_no_model = graph.add_relations(family_tree_no_model, "./data/family_no_model/"+name)        
        else:
            family_no_model = graph.get("./data/family_no_model/"+name)

        latex_tabell(name, family_no_model, family, silver)        

    print("MAIN DONE")


if __name__ == "__main__":
    if "data" not in os.listdir():
        os.makedirs("./data/character_bio")
        os.makedirs("./data/character_infobox")
        os.makedirs("./data/family_no_model")
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