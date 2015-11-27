import snap
import networkx as nx
import sys

argv.pop(0)
directory = argv.pop(0)
G = nx.read_edgelist(directory + 'Edge_List_Combined_' + item + '.txt')

# TODO: Generate itemNodeIds, userNodeIds
def predictLinksJaccard(GCombined, nodesAtHop, itemNodeIds, userNodeIds):
    nodesToNeighbors = {}
    for node in GCombined.Nodes():
        NodeVec = snap.TIntV()
        snap.GetNodesAtHop(GCombined, nodeId, 1, NodeVec, False)
        nodesToNeighbors[node] = NodeVec
        for item in NodeVec:
            print item
    
    scores = {} 
    for node1 in userNodeIds:
        for node2 in itemNodeIds:
            if not GCombined.isEdge(node1, node2):
                neigborsInCommon = len(set.intersection(set(nodesToNeighbors[node1]), set(nodesToNeighbors[node2])))
                neighborUnion = len(set.union(set(nodesToNeighbors[node1]), set(nodesToNeighbors[node2])))
                if not node1 in scores:
                    scores[node1] = {}
                scores[node1][node2] = float(neigborsInCommon)/float(neighborUnion)
            else: 
                if not node1 in scores:
                    scores[node1] = {}
                scores[node1][node2] = 0.0
                

def predictLinksNegatedShortestPath(GCombined, nodesAtHop, itemNodeIds, userNodeIds):
    scores = {} 
    for node1 in userNodeIds:
        for node2 in itemNodeIds:
            if not GCombined.isEdge(node1, node2):
                if not node1 in scores:
                    scores[node1] = {}
                scores[node1][node2] = 1.0/GetShortPath(GCombined, node1, node2, False)
            else:
                if not node1 in scores:
                    scores[node1] = {}
                scores[node1][node2] = 0.0
    
    
def predictLinksAdamicAdar(GCombined, nodesAtHop, itemNodeIds, userNodeIds):
    scores = nx.adamic_adar_index(G)