import spacy
import plac
import re
import sys

TEXT = """ 	  
Elrond Half-elven is the son of Eärendil and Elwing, and a great-grandson of Lúthien. 
He was born in the refuge of the Havens of Sirion in Beleriand late in the First Age, soon before its sack by the Sons of Fëanor. 
Elrond and his twin brother Elros were captured and raised by Maglor a Son of Fëanor. 
Though at first there was no great love between them, eventually Maglor took pity on them and cherished them, and eventually grew to love them.[1] 
By the end of the First Age and the War of Wrath, the Sons of Fëanor were again working alone, suggesting that by this time Elrond and Elros had left their nominal captivity and traveled to Lindon.
Test, Later, Elrond sent his sons Elladan, Arwen and Elrohir with the Rangers of the North to Rohan.
"""

#TODO BUG sometimes return 3 or more entities for one relation. Replicate by running 'Elrond'
def extract_relations(character_bio=TEXT):
    print("extract_relations")
    if character_bio == "":
        return None

    corpus = character_bio 
    #print(corpus)

    nlp = spacy.load("./model")#spacy.load("en_core_web_sm")
    doc = nlp(corpus)    
    for ent in doc.ents:    
        print(ent.text, ent.label_)

    relations = []

    child_of = re.compile(".*\b(is|was|had).*son.*")
    sibbling = re.compile(".*(brother|sister|twin).*")
    parent_to = re.compile(".*(his|her|had|has).*(sons?|daughter?).*")
    for sent in doc.sents:    
        ents = sent.ents
        for i in range(len(ents)):
            if i+1 < len(ents):            
                ent1 = ents[i] 
                ent2 = ents[i+1]

                if ent1.label_ == "PERSON" and ent2.label_ == "PERSON":                                
                    #TODO if verb in text_between then skip?

                    text_between = doc[ent1.end : ent2.start]                
                    if child_of.match(text_between.text):
                        relations.append((ent1.text, ent2.text, {"relation": "son_of", "text": str(sent)}))

                    elif sibbling.match(text_between.text):
                        relations.append((ent1.text, ent2.text, {"relation": "sibbling", "text": str(sent)}))

                    elif parent_to.match(text_between.text):
                        #sent.as_doc().print_tree()
                        relations.append((ent1.text, ent2.text, {"relation": "parent_to", "text":str(sent)}))                        
                        rels = listed_relation("parent_to", ent1, i, ents, sent, doc)
                        relations += rels                        
                            
    return relations

def listed_relation(relation_type, ent1, _i, ents, sent, doc):
    """ 
        Sometimes relations are listed, for example: "He was father to a, b, and c.
    """    
    relations = []
    i = _i + 1
    while i+1 < len(ents):         
        last_ent = ents[i]
        i += 1
        ent_n = ents[i]
        text_between = doc[last_ent.end: ent_n.start]        
        if text_between.text in ["and",","]:                               
            relations.append((ent1.text, ent_n.text, {"relation": relation_type, "text": str(sent)}))
    return relations


if __name__ == '__main__':
    rel = extract_relations()
    for r in rel:
        print(r)
        
    
    