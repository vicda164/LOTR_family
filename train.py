import os
import random
import numpy as np
import spacy
from collections import defaultdict

import filemanager


 
def create_train_data():
    training_set = [] #np.empty((1000, 5))
    nlp = spacy.load("en_core_web_sm")

    #list of existing names in LOTR    
    names = filemanager.lotr_char_names()
    print(len(names))
    filenames = os.listdir("data/character_bio/")
    filenames = ["Elrond.txt"] # TODO only for testing
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
    

                            entities.append(( start1_idx, end1_idx, "PERSON"))
                            entities.append(( start2_idx, end2_idx, "PERSON"))

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

    for t in training_set:
        print(t)
 
    return training_set



def train(train_set):
    # try simple implemantion from example on https://spacy.io/usage/training
    #TRAIN_DATA = [
    # ("Uber blew through $1 million a week", {'entities': [(0, 4, 'ORG')]}),
    # ("Google rebrands its business apps", {'entities': [(0, 6, "ORG")]})]

    nlp = spacy.load("en_core_web_sm")#spacy.blank('en')
    optimizer = nlp.begin_training()
    for i in range(len(train_set)):
        random.shuffle(train_set)
        for text, annotations in train_set:            
            #annotations = {"entities" : annotations} # adjust format            
            nlp.update([text], [annotations], sgd=optimizer)
    nlp.to_disk('./model')

    return None

if __name__ == '__main__':
    train_set = create_train_data()
    train(train_set)