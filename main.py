import plac
import numpy


import filemanager
import relation_extraction
import family_structure



# build relation tree

# bios_to_read
# read_bios


def find_family_relations(name, to_read=[], read_bios=[], relations=[]):
    print(name, to_read, read_bios, relations)
    if len(to_read) == 0:
        return relations

    char_bio = filemanager.getCharacterDescription(name)
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
    relatives = numpy.array(rel)[:,1] # get column 1
    relatives = [r for r in relatives if r not in read_bios]
    to_read += relatives

    return find_family_relations(to_read[0], to_read=to_read, read_bios=read_bios, relations=relations)




@plac.annotations(
    name=("Character name", "positional", None, str))
def run(name):  
    
    family_tree = find_family_relations(name, to_read=[name])
    family_structure.add_relations(family_tree)
    family_structure.draw_graph()

    for rel in family_tree:
        print(rel)   

if __name__ == "__main__":
    plac.call(run)