import json
import snap
from os import listdir
from os.path import isfile, join
from sys import argv

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
inFiles = ['cluster_123']

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
# 	idx = 1
# 	NIdV = snap.TIntV()
# 	for line in inputFile.readlines():
# 		if line[0] == '#':
# 			continue
# 		if idx > N:
# 			continue
# 		colon = line.split(':',1)
# 		clusterNum = int(colon[0])
# 		nodeId = int(colon[1].split()[-1])
# 		if not nodeId in nodeToCommunities: 
# 			nodeToCommunities[nodeId] = set()
# 		nodeToCommunities[nodeId].add(clusterNum)

# 		if not clusterNum in communitiesToNode:
# 			communitiesToNode[clusterNum] = set() 
# 		communitiesToNode[clusterNum].add(nodeId)

userToItems = {}
with open(directory + '_User_Item_' + item + '.txt', 'r') as infile4:
	userToItems = json.load(infile4)


usersGraph = snap.LoadEdgeList(snap.PUNGraph, directory + 'Edge_List_Users_' + item +'.txt', 0, 1, '\t')
itemsGraph = snap.LoadEdgeList(snap.PUNGraph, directory + 'Edge_List_Items_' + item +'.txt', 0, 1, '\t')

# Recommend 



# Compare against ground truth 
