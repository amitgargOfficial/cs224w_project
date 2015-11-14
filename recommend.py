import json
import snap
from os import listdir
from os.path import isfile, join
from sys import argv
import pickle

script, directory, item, inputDirectory = argv

graph = 'Users'

# Read in page rank scores 
pagerank = {}
with open(directory + 'Pagerank_' + graph + '_' + item +'.txt', 'r') as infile1:
    pagerank = json.load(infile1)


# Read in eigen centrality scores 
eigen_centrality = {}
with open(directory + 'Eigen_Value_' + graph + '_' + item +'.txt', 'r') as infile2:
    eigen_centrality = json.load(infile2)

# Read in nodesAtHop
inFiles = [f for f in listdir(inputDirectory) 
    if isfile(join(inputDirectory,f)) ]
# inFiles = ['cluster_100']

nodesAtHop = []
for filename in inFiles:
    with open(inputDirectory + filename, 'r') as infile3:
        curCluster = json.load(infile3)
    nodesAtHop.append(curCluster)

# filename = directory + '/Clusters_Users/Edge_List_' + graph + '_' + item + '.tree'

# # Read in communities 
# communitiesToNode = {}
# nodeToCommunities = {}
# N = 400
# with open(filename, 'r') as inputFile:
#   idx = 1
#   NIdV = snap.TIntV()
#   for line in inputFile.readlines():
#       if line[0] == '#':
#           continue
#       if idx > N:
#           continue
#       colon = line.split(':',1)
#       clusterNum = int(colon[0])
#       nodeId = int(colon[1].split()[-1])
#       if not nodeId in nodeToCommunities: 
#           nodeToCommunities[nodeId] = set()
#       nodeToCommunities[nodeId].add(clusterNum)

#       if not clusterNum in communitiesToNode:
#           communitiesToNode[clusterNum] = set() 
#       communitiesToNode[clusterNum].add(nodeId)

userToItems = {}
with open(directory + '_User_Item_' + item + '.txt', 'r') as infile4:
    userToItems = json.load(infile4)


usersGraph = snap.LoadEdgeList(snap.PUNGraph, directory + 'Edge_List_Users_' + item +'.txt', 0, 1, '\t')
itemsGraph = snap.LoadEdgeList(snap.PUNGraph, directory + 'Edge_List_Items_' + item +'.txt', 0, 1, '\t')

# PR, EIG
wtVec = [2.0, 1.5]

def dotProduct(vec):
    score = 0
    for idx in range(len(wtVec)):
        score += wtVec[idx]*vec[idx]
    return score

def updateDict(scores, hopDistance, queryUser, targetUser, items, alreadyBought):
    scale = 1.0/hopDistance
    pr = pagerank[targetUser]
    eig = eigen_centrality[targetUser]
    for item in items:
        if item in alreadyBought:
            continue
        if not item in scores:
            scores[item] = 0.0
        scores[item] += scale*dotProduct([pr,eig])
    return
    
N = 2 # How many predictions per user

# Recommend
userRecommendations = []
for community in nodesAtHop:
    userRecommendations.append({})
    for queryUser in community:
        scores = {} # Item -> Score
        allNbrs = community[queryUser]
        alreadyBought = userToItems[queryUser]
        for targetUser in allNbrs:
            boughtItems = userToItems[targetUser]
            hopDistance = allNbrs[targetUser]
            updateDict(scores, hopDistance, queryUser, targetUser, boughtItems, alreadyBought)
        srted = sorted(scores.iteritems(), key=lambda x:(-x[1],x[0]))
        topN = [x[0] for x in srted[:min(N,len(srted))]]
        userRecommendations[-1][queryUser] = topN
with open(directory + 'recommendations', 'wb') as outfile:
    pickle.dump(userRecommendations, outfile)
# Compare against ground truth 
