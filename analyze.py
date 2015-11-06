from os import listdir
from os.path import isfile, join
import networkx as nx

inputDir = '/Users/home/Desktop/Google Drive/Courses/224W/Project/Data/Unanalyzed Clusters/'
outputDir1 = '/Users/home/Desktop/Google Drive/Courses/224W/Project/Data/PageRanked Clusters/'
outputDir2 = '/Users/home/Desktop/Google Drive/Courses/224W/Project/Data/K - Cored Clusters/'

inFiles = [f for f in listdir(inputDir) 
	if isfile(join(inputDir,f)) ]

for clusterFile in inFiles:
	G = read_weighted_edgelist(clusterFile, comments='#', nodetype = float)
	
	# Pagerank
	pagerank = nx.pagerank(G, weight='weight') # Returns dictionary

	f = open(outputDir1 + clusterFile, 'w')
	for key, value in pagerank:
		f.write(key + '\t' + value +'\n')
	
	# Set k value
	nodes = G.nodes()
	for node in nodes:
		k += G.degree(node)
	k /= len(nodes)
	print clusterFile, k
	subG = k_core(G, k=None) # Returns subgraph
	nx.write_weighted_edgelist(subG, outputDir2 + clusterFile, 'w')