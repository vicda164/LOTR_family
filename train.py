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



def train(train_set, model="en_core_web_sm"):
    # try simple implemantion from example on https://spacy.io/usage/training
    #TRAIN_DATA = [
    # ("Uber blew through $1 million a week", {'entities': [(0, 4, 'ORG')]}),
    # ("Google rebrands its business apps", {'entities': [(0, 6, "ORG")]})]

    nlp = spacy.load(model) #spacy.blank('en')    
    optimizer = nlp.begin_training()
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    print("0 of", len(train_set))
    with nlp.disable_pipes(*other_pipes):  # only train NER
        for i in range(len(train_set)):
            random.shuffle(train_set)
            for text, annotations in train_set:            
                #annotations = {"entities" : annotations} # adjust format            
                annotations = ast.literal_eval(annotations)
                try:
                    nlp.update([text], [annotations], sgd=optimizer)
                except Exception as identifier:
                    print("ERROR:", str(identifier))
                    nlp.to_disk('./model')
            
            if i % 10 == 0:
                print(i,"of",len(train_set))

    nlp.to_disk('./model')
    return "OK"

if __name__ == '__main__':
    #train_set = create_train_data()
    #filemanager.writeCSV("./train_set_val", train_set, delimiter="|",quotechar='"')
    #train_set = filemanager.readCSV("./train_set", delimiter="|",quotechar='"')
    #train(train_set)
    s = [("Elrond Half-elven is the son of Eärendil and Elwing, and a great-grandson of Lúthien.","{'entities': [(0, 17, 'PERSON'), (77, 84, 'PERSON'),(32, 40, 'PERSON'), (45, 51, 'PERSON')]}")]
    train(s, "./model")
    