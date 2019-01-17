import ast
import os
import random
from collections import defaultdict


import numpy as np
import spacy

import filemanager

def create_train_data():
    training_set = [] #np.empty((1000, 5))
    nlp = spacy.load("en_core_web_sm")

    #list of existing names in LOTR    
    names = filemanager.lotr_char_names()
    #print(len(names))
    filenames = os.listdir("data/character_bio/")
    filenames = ["Elrond.txt","Elros.txt", "Arwen.txt","Aragorn II Elessar.txt", "Galadriel.txt"] # TODO only for testing
    count = defaultdict(int)
    for filename in filenames:
        filename = "data/character_bio/" + filename
        biography = filemanager.getFromText(filename)
        doc = nlp(biography)

        for sentance in doc.sents:
            entities = []
            for name in names:
                # TODO: if a character name occur that we don't have in Names then we will make the NER worse by training
                # Don't collect more than 10 sample of same name                
                #if count[name] > 10:
                    #names.remove(name) # can't remove from from np.array
                #    continue
                
                if name in sentance.text:
                    #print(name, ":" ,sentance.text)
                    ent = [e for e in sentance.ents if name in e.text]
                    if len(ent) > 0:
                        # This is needed because if the NER is not recongnised correctly
                        ent = ent[0]
                        position = sentance.start_char
                        if "and" in ent.text: #TODO if "and" in ent "Eärendil and Elwing"
                            name1 = ent.text.split("and")[0]
                            name2 = ent.text.split("and")[-1]

                            start1_idx = ent.start_char - position
                            end1_idx = ent.end_char - position

                            start2_idx = ent.end_char + 4 #'and '
                            end2_idx = start2_idx + len(name2)
                            count[name1] += 1
                            count[name2] += 1

                            entities.append((start1_idx, end1_idx, "PERSON"))
                            entities.append((start2_idx, end2_idx, "PERSON"))

                        else:
                            #print("EXIST:",name, doc[ent.start], doc[ent.end] , sentance)
                            count[name] += 1
                            
                            start_idx = ent.start_char - position
                            end_idx = ent.end_char - position                        
                            #training_set.append([str(sentance), (name, start_idx, end_idx, "PERSON")])
                            # depening on how we train the format seems to differ slightly
                            
                            entities.append((start_idx, end_idx, "PERSON"))

            if len(entities) > 0:
                training_set.append([str(sentance),  {"entities" : entities}])

    #for t in training_set:
    #    print(t)
 
    print(count)
    return training_set



def train(train_set, save_to, model="en_core_web_sm"):
    # save_to = "./model"
    # try simple implemantion from example on https://spacy.io/usage/training
    #TRAIN_DATA = [
    # ("Uber blew through $1 million a week", {'entities': [(0, 4, 'ORG')]}),
    # ("Google rebrands its business apps", {'entities': [(0, 6, "ORG")]})]

    nlp = spacy.load(model) #spacy.blank('en')    
    optimizer = nlp.begin_training()
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    print("0 of", len(train_set))
    with nlp.disable_pipes(*other_pipes):  # only train NER
        for i in range(5*len(train_set)):
            random.shuffle(train_set)
            for text, annotations in train_set:            
                #annotations = {"entities" : annotations} # adjust format            
                try:
                    annotations = ast.literal_eval(annotations)
                except Exception as identifier:
                    print("ERROR: bad format: ", text)
                    return
                
                try:
                    nlp.update([text], [annotations], sgd=optimizer)
                except Exception as identifier:
                    print("ERROR:", str(identifier))
                    nlp.to_disk(save_to)
            
            if i % 10 == 0:
                print(i,"of",len(train_set))

    nlp.to_disk(save_to)
    return "OK"

if __name__ == '__main__':
    #train_set = create_train_data()
    #filemanager.writeCSV("./train_set_val", train_set, delimiter="|",quotechar='"')
    #train_set = filemanager.readCSV("./train_set", delimiter="|",quotechar='"')
    #train(train_set)
    s = [("Celebrían (IPA: [keleˈbriːan]) was an Elven noblewoman, the daughter of Celeborn and Galadriel, wife of Elrond, and mother of Elrohir, Elladan and Arwen. ","{'entities': [(0, 9, 'PERSON'), (72,80,'PERSON'), (85,94,'PERSON'),(104,110,'PERSON'),(126,133,'PERSON'),(135,142, 'PERSON'),(147,152, 'PERSON')]}"),
 ("They included three sons, Vardamir Nólimon, Manwendil, and Atanalcar, and a daughter, Tindómiel.","{'entities': [(59, 68, 'PERSON'), (44, 53, 'PERSON'), (26, 42, 'PERSON'),(86,95,'PERSON')]}"),
 ("Besides Aragorn, Gandalf, and Frodo, the company included Frodo's cousins Pippin and Merry, his best friend Samwise Gamgee, Legolas the elf, Gimli the Dwarf, and Boromir of Gondor. Before the group set out, the shards of Narsil were reforged, and the restored blade was named Andúril.", "{'entities': [(8,15,'PERSON'),(17,24, 'PERSON'), (30,35,'PERSON'),(58,63,'PERSON'),(74,80,'PERSON'),(85,90,'PERSON'),(108,122,'PERSON'), (124, 131, 'PERSON'),(141,146,'PERSON'),(162, 169, 'PERSON')]}"),
 ("Elrond Half-elven is the son of Eärendil and Elwing, and a great-grandson of Lúthien.", "{'entities': [(0, 17, 'PERSON'), (77, 84, 'PERSON'),(32, 40, 'PERSON'), (45, 51, 'PERSON')]}"),
 ("Argon was the younger brother of Fingon, Turgon, and Aredhel his elder sister.", "{'entities': [(0, 5, 'PERSON'), (33, 49, 'PERSON'),(41, 47, 'PERSON'), (53, 60, 'PERSON')]}")]
    train(s, save_to="./model_slim", model="./model_slim")
    