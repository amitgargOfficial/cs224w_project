import snap
from sys import argv
import pickle
import networkx

# TODO: Generate itemNodeIds, userNodeIds
def predictLinksJaccard(GCombined, nodesAtHop, itemNodeIds, userNodeIds, directory):
    nodesToNeighbors = {}
    for node in GCombined.Nodes():
        NodeVec = snap.TIntV()
        snap.GetNodesAtHop(GCombined, node.GetId(), 1, NodeVec, False)
        nodesToNeighbors[node] = NodeVec
    
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
    with open(directory + 'Jaccards', 'wb') as outfile:
        pickle.dump(scores, outfile)
                

def predictLinksNegatedShortestPath(GCombined, nodesAtHop, itemNodeIds, userNodeIds, directory):
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
    with open(directory + 'NegatedShortestPath', 'wb') as outfile:
        pickle.dump(scores, outfile)
    
def predictLinksAdamicAdar(GCombined, nodesAtHop, itemNodeIds, userNodeIds, directory):
    scores = {}
    preds = nx.adamic_adar_index(G)
        
    for u, v, p in preds:
        if not u in scores:
            scores[u] = {}
        scores[u][v] = p
    
    with open(directory + 'AdamicAdar', 'wb') as outfile:
        pickle.dump(scores, outfile)
    