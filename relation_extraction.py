import re
import sys
import os

from spacy import displacy
import spacy
import plac

TEXT = """ 	  
Elrond Half-elven is the son of Eärendil and Elwing, and a great-grandson of Lúthien. 
He was born in the refuge of the Havens of Sirion in Beleriand late in the First Age, soon before its sack by the Sons of Fëanor. 
Elrond and his twin brother Elros were captured and raised by Maglor a Son of Fëanor. 
Though at first there was no great love between them, eventually Maglor took pity on them and cherished them, and eventually grew to love them.[1] 
By the end of the First Age and the War of Wrath, the Sons of Fëanor were again working alone, suggesting that by this time Elrond and Elros had left their nominal captivity and traveled to Lindon.
Later, Elrond sent his sons Elladan and Elrohir with the Rangers of the North to Rohan.
"""

TEXT2 = """
Aragorn, Legolas and Gimli then help the people of Rohan in the Battle of the Hornburg, in which they conclusively and victoriously defeated Saruman's army.[15]
"""

TEXT3 = """
  Elrond (Sindarin; IPA: "Star-Dome") Half-elven, Lord of Rivendell, 
  was one of the mighty Elf-rulers of old who lived in Middle-earth from the First Age to the beginning of the Fourth Age.
  He was the father of Arwen Undomiel, lover of Aragorn II Elessar.
  Elrond Half-elven is the son of Eärendil and Elwing, and a great-grandson of Lúthien. He was born in the refuge of the Havens of Sirion in Beleriand late in the First Age, soon before its sack by the Sons of Fëanor. Elrond and his twin brother Elros were captured and raised by Maglor a Son of Fëanor. Though at first there was no great love between them, eventually Maglor took pity on them and cherished them, and eventually grew to love them.[1] By the end of the First Age and the War of Wrath, the Sons of Fëanor were again working alone, suggesting that by this time Elrond and Elros had left their nominal captivity and traveled to Lindon. Elrond and Elros were given the choice at the end of the First Age to be counted among Men or Elves. Elros chose the Fate of Men and became Elros Tar-Minyatur, the first King of Númenor. Elrond chose to be counted among the Elves,[2] and remained in Lindon as captain and herald of Gil-Galad, the High King of the Ñoldor.[3] In SA 1695, Elrond was sent to Eregion by Gil-galad in an attempt to protect it from the invading forces of Sauron. Unfortunately, Elrond's host was too weak and was unable to hold off Sauron's army. He retreated north with a host of elves out of Eregion including Celeborn and remained ever watchful of Sauron from there. It was during the following two years (SA 1697) that Elrond founded Rivendell at the feet of the Misty Mountains, which survived as one of the last remaining strongholds against Sauron at the end of the Third Age.[4][5] After the combined forces of the elves under Gil-Galad, Cirdan, Elrond and the Men of Númenor defeated Sauron in SA 1701 Elrond remained in Rivendell and hosted the first White Council, attended by Galadriel, at which it was decided that Elrond's home, the Last Homely House, would remain the last stronghold west of the Misty Mountains, and that the Three Rings then held by Gil-Galad and Galadriel would remain hidden. According to one account Gil-Galad at this time gave Elrond Vilya the Blue Ring, though in other accounts Gil-Galad kept both Narya and Vilya until the end of the Second Age. It was also here that Elrond first met Celebrían, the daughter of Celeborn and Galadriel. Near the end of the Second Age, Elrond rode beside Gil-Galad in the Last Alliance of Elves and Men, which set out from Rivendell to Mordor in SA 3431. Elrond was Gil-galad's herald during the war against Sauron. The Alliance, which also included elves from Lorien, men from Arnor and Gondor, and Dwarves led by Durin lV, eventually defeated Sauron's army and laid siege to Barad-dûr for seven years. Eventually, Sauron himself was defeated by Elendil and Gil-galad, allowing Isildur to cut the One Ring from Sauron's finger and claim the Ring for himself. The Last Alliance of Elves and Men took a toll on the forces of both Elves and Men. Gil-Galad, Elendil, and his younger son Anarion were killed in the siege. Elrond and Cirdan only remained as the commanders of the elves, and Isildur as lord of men. Upon discovering that Isildur had claimed the One Ring for himself Elrond urged Isildur to throw the Ring into the fires of Mount Doom, but the seduction of the ring made Isildur refuse. Isildur claimed the Ring as a Weregild for his father and brother, and Elrond (perhaps not fully understanding the nature of the One Ring) acknowledged his claim. Isildur was then named High King of Gondor and Arnor and took his father's throne, while Elrond returned to Rivendell at the end of the war.[4] In the year TA 109, Elrond wedded Celebrían. In the year TA 130, the twins Elladan and Elrohir were born, and in TA 241 a daughter, Arwen Undómiel. Elrond lost Celebrían in TA 2510 when she was waylaid by orcs crossing the Misty Mountains and, unable to recover, took a ship to the Undying Lands.[6][7] In the later years, he was instrumental in harboring the heirs of Isildur while the line lasted, the most famous of these sons of men was Aragorn son of Arathorn II, whom he took in and fostered as his own after his father died in TA 2933. Elrond, foreseeing the boy's difficult future gave him the name Estel, Sindarin for Hope. Aragorn grew up in Imladris unaware of his kingly lineage until Elrond told him when he had reached his manhood.[8] He also was a member of the White Council, which was often held in Rivendell, and was a great friend of Gandalf the Grey. He helped Thorin Oakenshield's expedition to retake the Lonely Mountain by discovering and translating the Moon Writing on Thorin's map.[9] After Frodo's departure from the Shire with the One Ring, Elrond sent out riders to help guide him back to Rivendell. One of these, Glorfindel, successfully found Frodo and helped him reach Rivendell.[10] On October 25, 3018 he held the Council at which it was decided to attempt to destroy the One Ring. He appeared to have selected the members of the Fellowship other than Frodo and Sam.[11] Later, Elrond sent his sons Elladan and Elrohir with the Rangers of the North to Rohan. Through his sons, Elrond advised Aragorn to take the Paths of the Dead.[12] Elrond remained in Rivendell until the destruction of the One Ring and of Sauron, after which he went to Minas Tirith to surrender the Sceptre of Annúminas to King Elessar and give his daughter Arwen Undómiel away to be married.[13] On September 29, 3021, Elrond left Middle-earth to go over the sea with the other Ring-bearers, never to return.[14]
"""

TEXT4 = "Celebrían (IPA: [keleˈbriːan]) was an Elven noblewoman, the daughter of Celeborn and Galadriel, wife of Elrond, and mother of Elrohir, Elladan and Arwen."

#TODO BUG sometimes return 3 or more entities for one relation. Replicate by running 'Elrond'
def extract_relations(character_bio=TEXT, model="./model"):
    print("extract_relations")
    if character_bio == "":
        return None

    corpus = character_bio 
    #print(corpus)

    """
    if len(os.listdir(model) != 0:
        nlp = spacy.load(model)
    else:
        nlp = spacy.load("en_core_web_sm")
    """
    nlp = spacy.load(model)
    doc = nlp(corpus)    
    #for ent in doc.ents:    
    #    print(ent.text, ent.label_)

    relations = []

    child_of = re.compile(r".*\b(is|was|had).*(son|daughter).*|.*(son|daughter) of .*")
    sibbling = re.compile(r".*(brother|sister|twin).*")
    parent_to = re.compile(r".*(his|her|had|has).*(sons?|daughter?)|.*(mother|father) (to|of).*")
    spouse = re.compile(r".*(wife|husband|married to|wedded).*")
    for sent in doc.sents:    
        ents = sent.ents
        #sent.text.replace("he", name) #TODO: should it be a good idea to replace?
        for i in range(len(ents)):
            if i+1 < len(ents):            
                ent1 = ents[i] 
                ent2 = ents[i+1]

                if ent1.label_ == "PERSON" and ent2.label_ == "PERSON":                                
                    #TODO if verb in text_between then skip?

                    text_between = doc[ent1.end : ent2.start]                
                    if child_of.match(text_between.text):
                        relations.append((ent1.text, ent2.text, {"relation": "child", "text": str(sent)}))
                        rels = listed_relation("child", ent1, i, ents, sent, doc)
                        relations += rels

                    elif sibbling.match(text_between.text):
                        relations.append((ent1.text, ent2.text, {"relation": "sibling", "text": str(sent)}))
                        rels = listed_relation("sibling", ent1, i, ents, sent, doc)
                        relations += rels

                    elif parent_to.match(text_between.text):
                        #sent.as_doc().print_tree()
                        relations.append((ent1.text, ent2.text, {"relation": "parent", "text":str(sent)}))                        
                        rels = listed_relation("parent", ent1, i, ents, sent, doc)
                        relations += rels

                    elif spouse.search(text_between.text):
                        relations.append((ent1.text, ent2.text, {"relation": "spouse", "text": str(sent)}))
                            
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


def test_NER(model="en_core_web_sm"):
    """
        Visualizing NER.
    """
    nlp = spacy.load(model)
    doc = nlp(TEXT)
    svg = displacy.render(doc, style='ent')
    file_name = 'NER_before_training.svg'
    output_path = './report_data/' + file_name
    open(output_path, 'w', encoding='utf-8').write(svg)
    displacy.serve(doc, style='ent')
    print(extract_relations(TEXT, model))

    
if __name__ == '__main__':
    test_NER("./model")    
    test_NER()
    