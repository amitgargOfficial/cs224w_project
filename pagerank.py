import snap
import json

item = 'Users_Cell_Phones_and_Accessories'

G = snap.LoadEdgeList(snap.PUNGraph, 'Edge_List_' + '.txt', 0, 1, '\t')

dict = {}
PRankH = snap.TIntFltH()
snap.GetPageRank(G, PRankH)
for item in PRankH:
    dict[item] = PRankH[item]

with open('pagerank_'+ 'Users_Cell_Phones_and_Accessories' +'.txt', 'w') as outfile:
	json.dump(dict, outfile)