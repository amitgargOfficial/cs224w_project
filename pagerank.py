import snap
import json

directory = '/Users/home/Desktop/Google Drive/Courses/224W/Project/Data/'
item = 'Cell_Phones_and_Accessories'
graph = 'Items'

G = snap.LoadEdgeList(snap.PUNGraph, directory + 'Edge_List_' + graph + '_' + item +'.txt', 0, 1, '\t')

snap.PrintInfo(G, 'Graph Info')

dict = {}
PRankH = snap.TIntFltH()
snap.GetPageRank(G, PRankH)
for item in PRankH:
    dict[item] = PRankH[item]

with open('pagerank_' + graph +'_Cell_Phones_and_Accessories' +'.txt', 'w') as outfile:
	json.dump(dict, outfile)