import random
from math import sqrt
import triangle as triangle
import matplotlib.pyplot as plt
from sys import argv
import re





class Point:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init

    def shift(self, x, y):
        self.x += x
        self.y += y

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])


def distance(a, b):
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


list_of_vertices = []
# for i in range(100):
#     x = random.randint(-20, 20)
#     y = random.randint(-20, 20)
#     list_of_vertices.append(Point(x, y))
# for i, item in enumerate(list_of_vertices):
#     print(item.__repr__())
# f = open('test.poly', 'w')
# for i, item in enumerate(list_of_vertices):
#     f.write(' ' + str(i) + '   ' + str(item.x) + ' ' + str(item.y) + '\n')
# f.write('0 0\n')
# f.write('0')
# f.close()
for i in range(100):
    x = random.randint(-20, 20)
    y = random.randint(-20, 20)
    list_of_vertices.append([x, y])
print(list_of_vertices)
s = []
for i in range(100):
    for j in range(100):
        s.append([i, j])
A = dict(vertices=list_of_vertices, segments=s)
t = triangle.triangulate(A, 'e')
edges = t['edges'].tolist()
for i, item in enumerate(edges):
    item.append(distance(Point(list_of_vertices[item[0]][0], list_of_vertices[item[0]][1]), Point(list_of_vertices[item[1]][0], list_of_vertices[item[1]][1])))
print(edges)
triangle.compare(plt, A, t)
plt.show()
# print(t.values())


# A = dict(vertices=list_of_vertices)
# t = triangle.delaunay(list_of_vertices)
# print(t.tolist())
# plt.show()




f = open('graph1.wug', 'w')
# f.write('// WEIGHTED UNDIRECTED GRAPH FILE\n// Structure:\n// (node-1)(space)(node-2)(space)(distance)\n')
for i, item in enumerate(edges):
    f.write(str(item[0]) + ' ' + str(item[1]) + ' ' + str(item[2]) + ' \n')
f.close()

greatest_node = -1.0
# Graph list
graph = []
file = open('graph1.wug', "r")
for line in file:
    # Reading only lines there are not comments
    if not re.match("//", line):
        info = line.split(" ")
        # Create JSON and remove \n of end of line
        arrest = {info[0] + "&" + info[1]: info[2].replace('\n', '')}
        # Calcuting the greatest node
        if float(info[0]) > greatest_node:
            greatest_node = float(info[0])
        if float(info[1]) > greatest_node:
            greatest_node = float(info[1])
            # Add JSON to graph
        graph.append(arrest)
# n = number max of nodes
nodes = greatest_node + 1.0
# Set MST with a random value
# List with the result
prim = []
# Auxiliar JSON to find the closest distance
min_dist = {}
# List of added nodes
added = []
# Add the arbitray first node on added list
added.append(float(list(graph[0].keys())[0].split("&")[0]))
i = 0
while i < nodes:
    for node in range(len(graph)):
        n = list(graph[node].keys())[0].split("&")
        # Filter the nodes that can be added
        # At lest n[0] or n[1] must be added to this node be a candidate
        # And one of them must be not added before
        if (float(n[0]) in added or float(n[1]) in added) and (float(n[0]) not in added or float(n[1]) not in added):
            # If closest distance is empty, then
            if len(min_dist) == 0:
                min_dist = graph[node]
            # If the node distance is smaller than min_dist
            elif float(list(graph[node].values())[0]) < float(list(min_dist.values())[0]):
                min_dist = graph[node]
    # Append
    if min_dist:
        prim.append(min_dist)
        if float(list(min_dist.keys())[0].split("&")[0]) not in added:
            added.append(float(list(min_dist.keys())[0].split("&")[0]))

        if float(list(min_dist.keys())[0].split("&")[1]) not in added:
            added.append(float(list(min_dist.keys())[0].split("&")[1]))
    # Reset variable
    min_dist = {}
    # Look for next node
    i += 1
# Final report
print("-- MST nodes --")
print(prim)
print("-- Final cost --")
cost = 0
for i in prim:
    if i:
        cost += float(list(i.values())[0])
print(cost)