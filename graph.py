import os

import networkx as nx
import matplotlib.pyplot as plt

def add_relations(relations, file="./data/edgelist"):
    """
        names: simple list with all names
        relations: list of tuples (nameA, nameB, relationAtoB, text_from_extraction)
    """
    # TODO Check if file exists
    #print("Add relations")
    if not os.path.exists(file):
        #create a directed graph which can have multiple edges between two nodes
        graph = nx.MultiDiGraph()
        with open(file, 'w'): pass
    else:
        graph = nx.read_edgelist(file, delimiter="|", create_using=nx.MultiDiGraph())

    
    try:
        graph.add_edges_from(relations)    
    except Exception as identifier:
        print(relations)
        print("Error: ", str(identifier))        
    
    #print(graph.edges)

    try:
        nx.write_edgelist(graph, file, delimiter="|")
    except Exception as identifier:
        print("ERROR:" , str(identifier))
    
    return graph.edges(data=True)


def get(file):
    #print("get_family_tree", file)
    graph = nx.read_edgelist(file, delimiter="|").edges(data=True)
    #print(graph)
    return graph

def draw(file, file2=None):    
    graph = nx.read_edgelist(file, delimiter="|", create_using=nx.Graph())
    if file2 != None:
        plt.subplot()

    pos = nx.spring_layout(graph)
    
    edge_labels=dict([((u,v,),d['relation'])
             for u,v,d in graph.edges(data=True)])
    
    #edge_labels = nx.get_edge_attributes(graph, 'relation')    
    nx.draw(graph, pos=pos, with_labels=True, font_weight='bold', font_size=14)

    nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=edge_labels, font_size=16)
    plt.show()

    if file2 != None:
        plt.subplot()
        g2= nx.read_edgelist(file2, delimiter="|", create_using=nx.Graph())
        pos2 = nx.spring_layout(g2)
        #edge_labels = nx.get_edge_attributes(g2, 'relation')
        edge_labels=dict([((u,v,),d['relation'])
             for u,v,d in g2.edges(data=True)])

        nx.draw(g2, pos=pos2, with_labels=True, font_weight='bold', node_color="b")

        nx.draw_networkx_edge_labels(g2, pos=pos2, edge_labels=edge_labels)

    #nx.draw_shell(g, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
    plt.show()

if __name__ == '__main__':
    #add_relations([("Sansa", "Jon", {"relation":"siblings", "text":"text bla bla"})])
    #draw_graph()
    get("data/character_infobox/Elrond")


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
