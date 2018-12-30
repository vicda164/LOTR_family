import os

import networkx as nx
import matplotlib.pyplot as plt

def add_relations(relations, file="./data/edgelist"):
    """
        names: simple list with all names
        relations: list of tuples (nameA, nameB, relationAtoB, text_from_extraction)
    """
    # TODO Check if file exists
    print("Add relations")
    if not os.path.exists(file):
        graph = nx.Graph()
        with open(file, 'w'): pass
    else:
        graph = nx.read_edgelist(file, delimiter="|")#, data=(("realtion", str),("text",str),))

    
    try:
        graph.add_edges_from(relations)    
    except Exception as identifier:
        print(relations)
        print("Error: ", str(identifier))        
    
    print(graph.edges)
    nx.write_edgelist(graph, file, delimiter="|")#, data=(("realtion", str),("text",str),))
    return graph


def get_family_tree(file):
    #print("get_family_tree", file)
    graph = nx.read_edgelist(file, delimiter="|").edges(data=True)
    #print(graph)
    return graph

def draw_graph(file, file2=None):
    graph = nx.read_edgelist(file, delimiter="|")
    pos = nx.spring_layout(graph, scale=2)
    edge_labels = nx.get_edge_attributes(graph, 'relation')

    nx.draw(graph, with_labels=True, font_weight='bold')

    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    if file2 != None:
        g2= nx.read_edgelist(file, delimiter="|")
        pos = nx.spring_layout(g2, scale=2)
        edge_labels = nx.get_edge_attributes(g2, 'relation')

        nx.draw(g2, with_labels=True, font_weight='bold')

        nx.draw_networkx_edge_labels(g2, pos, edge_labels=edge_labels)

    #nx.draw_shell(g, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
    plt.show()

if __name__ == '__main__':
    #add_relations([("Sansa", "Jon", {"relation":"siblings", "text":"text bla bla"})])
    #draw_graph()
    get_family_tree("data/character_infobox/Elrond")


"""
# Some exaple code
g = nx.Graph()
g.add_nodes_from(["Elrond", "Elros", "Elbabe", "Arwen", "Arwen2", "Arwen3","Rick","Morty"])
g.add_edge("Elrond", "Elros", relation="Sibling", text="Elrond and his twin brother Elros")
g.add_edge("Elrond", "Elbabe", relation="Spouse")
g.add_edge("Elbabe", "Elrond", relation="Spouse")
g.add_edge("Elrond", "Arwen", relation="Child")
g.add_edge("Elrond", "Arwen2", relation="Child")
g.add_edge("Elrond", "Arwen3", relation="Child")
g.add_edge("Rick", "Morty", relation="GrandParent")
print(g.nodes)
print(list(g.edges))

# plot the graph
pos = nx.spring_layout(g, scale=2)
edge_labels = nx.get_edge_attributes(g, 'relation')


#G = nx.petersen_graph()
#plt.subplot(121)

nx.draw(g, with_labels=True, font_weight='bold')
#plt.subplot(122)

nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
#nx.draw_shell(g, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show()

nx.write_edgelist(g, "./data/edgelist")

g2 = nx.read_edgelist("./data/edgelist")
nx.draw(g2, with_labels=True, font_weight='bold')
#plt.subplot(122)

nx.draw_networkx_edge_labels(g2, pos, edge_labels=edge_labels)
#nx.draw_shell(g, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show()
"""

#class FamilyGraph:    
#    def __init__(self):    
#        self.graph = nx.read_edgelist("./data/edgelist")
