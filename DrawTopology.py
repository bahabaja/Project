import networkx
import matplotlib.pyplot

# Open the temporary empty file to get the adjaceny info
adjacencies  = open('/home/debian/cdptempoutput.txt' , 'r')
# Creata a graph
graph = networkx.Graph()
#Initilaize empty tuple and emptylist
tuple1 = ()
elist = []
# Get the tuples from file
for line in adjacencies:
    node1 = line.split(',')[0]
    node2 = line.split(',')[1]
    node2x = node2.replace('\n','')
    tuple1 = (node1,node2x)
    elist.append(tuple1)
# Remove the same edges from the list
for item in elist:
    revitem = tuple(reversed(item))
    if revitem in elist:
        elist.remove(revitem)
# Add nodes and edges to the graph
for i in elist:
    graph.add_node(i[0])
    graph.add_edge(i[0],i[1])
# Draw the graph
networkx.draw(graph, with_labels = True)
matplotlib.pyplot.show()