import sys
import gzip
import snap
import time
import json
import math 


GItems = snap.TUNGraph.New()
userEdges = []
years = [2008, 2009]
asinItems = {} # Key (string) is the asin of the item and value is the nodeId (int) in the graph

GUsers = snap.TUNGraph.New()

nodeIdUsers = {} # Key is the nodeId (int) in the graph and value (string) is the reviewerID of the user
reviewerIdUsers = {} # Key (string) is the reviewerID of the user and value is the nodeId (int) in the graph

def parseIterator(path):
	g = gzip.open(path, 'r')
	for l in g:
		yield eval(l)

def parseItems(path):
	# Adding nodes to GItems
	itemsNodeId = 0
	for item in parseIterator(path):
		# Adding nodes to GItems
		GItems.AddNode(itemsNodeId)
		asinItems[item['asin']] = itemsNodeId
		itemsNodeId +=1

	# Adding edges to GItems
	for itemSrc in parseIterator(path):
		try: # Some items do not have related or bought_together
			related = itemSrc['related']
			for itemDstAsin in related['bought_together']:
				if asinItems[itemDstAsin] is not None: # Some bought_together items are not present in nodes
					GItems.AddEdge(asinItems[itemDstAsin], asinItems[itemSrc['asin']])
		except KeyError:
			pass

def parseReviews(path, goodRating):
	# Adding nodes to GUsers
	usersNodeId = 0
	for review in parseIterator(path):
		# Adding nodes to GUsers
		year = review['reviewTime'].split()
		if int(year[2]) in years:
			reviewerId = reviewerIdUsers.get(review['reviewerID'])
			if reviewerId is None:
				GUsers.AddNode(usersNodeId)
				nodeIdUsers[usersNodeId] = review['reviewerID']
				reviewerIdUsers[review['reviewerID']] = usersNodeId
				usersNodeId += 1

	# Adding edges to GUsers
	for i in range(0, GUsers.GetNodes()):
		userEdges.append([])
		for j in range(0, GUsers.GetNodes()):
			userEdges[i].append((0.0, 0))

	reviewersByAsin = {}
	for review in parseIterator(path):
	# Adding nodes to GUsers
		year = review['reviewTime'].split()
		rating = review['overall']
		if int(year[2]) in years and rating >= goodRating:
			user = reviewerIdUsers[review['reviewerID']]
			asin = review['asin']
			if asin in reviewersByAsin:	
				reviewersByAsin[asin].append((user, rating))		
			else:
				reviewersByAsin[asin] = []
				reviewersByAsin[asin].append((user, rating))    
			
	for key in reviewersByAsin:
		for (user1, rating1) in reviewersByAsin[key]:
			for (user2, rating2) in reviewersByAsin[key]:
				if user1 != user2:
					userEdges[user1][user2] = (userEdges[user1][user2][0] + math.pow(3.0 - math.fabs(rating1 - rating2), 2), userEdges[user1][user2][1] + 1)
					userEdges[user2][user1] = (userEdges[user2][user1][0] + math.pow(3.0 - math.fabs(rating1 - rating2), 2), userEdges[user2][user1][1] + 1)
	
	for user1 in range(0, len(userEdges)):
		for user2 in range(0, len(userEdges)):
			if userEdges[user1][user2][1] > 0:
				GUsers.AddEdge(user1, user2)
				

	#users = []
	#reviews = parseIterator(path)
	#while True: # Adding the first user with overall > goodRating
	#	reviewFirst = reviews.next()
	#	if int(reviewFirst['overall']) >= goodRating:
	#		year = reviewFirst['reviewTime'].split()
	#		if int(year[2]) == 2011 or int(year[2]) == 2012:
	#			break
	#asinCompare = reviewFirst['asin']
	#users.append(reviewerIdUsers[reviewFirst['reviewerID']])
	#while True:
	#	try:
	#		while True:
	#			review = reviews.next()
	#			if int(review['overall']) >= goodRating:
	#				year = review['reviewTime'].split()
	#				if int(year[2]) == 2011 or int(year[2]) == 2012:
	#					break
	#		if review['asin'] == asinCompare:
	#			users.append(reviewerIdUsers[review['reviewerID']])
	#		else:
	#			for userSrcIndex in range(0, len(users)):
	#				for userDstIndex in range(userSrcIndex+1, len(users)):
	#					GUsers.AddEdge(users[userSrcIndex], users[userDstIndex])
	#			users[:] = []
	#			asinCompare = review['asin']
	#			users.append(reviewerIdUsers[review['reviewerID']])
	#	except StopIteration:
	#		for userSrcIndex in range(0, len(users)):
	#				for userDstIndex in range(userSrcIndex+1, len(users)):
	#					GUsers.AddEdge(users[userSrcIndex], users[userDstIndex])
	#		break
		
def main(argv):
	#directory = '/Users/home/Desktop/Google Drive/Courses/224W/Project/Data/'
	directory = '/Users/home/Desktop/Google Drive/Courses/224W/Project/Data/'
	item = 'Cell_Phones_and_Accessories'
	goodRating = 5

	# Parsing Items
	parseItems(directory + 'meta_' + item + '.json.gz')
	
	snap.PrintInfo(GItems, 'GItems Information')
		  
	# Saving GItems
	snap.SaveEdgeList(GItems, directory + 'Edge_List_Items_' + item + '.txt')

	with open(directory + 'Dictionary_Items_' + item + '.txt', 'w') as f1:
		json.dump(asinItems, f1)

	# Parsing Reviews
	#parseReviews(directory + 'reviews_' + item + '.json.gz', goodRating)
	
	snap.PrintInfo(GUsers, 'GUsers Information')

	# Saving GUsers
	#snap.SaveEdgeList(GUsers, directory + 'Edge_List_Users_' + item + '.txt')
	f = open('Edge_List_Users_' + item + '.txt', 'w')
	for edge in GUsers.Edges():
		srcNId = edge.GetSrcNId()
		dstNId = edge.GetDstNId()
		weight = userEdges[srcNId][dstNId][0]/float(userEdges[srcNId][dstNId][1])
		f.write('%d %d %f\n' % (srcNId, dstNId, weight))

	with open(directory + 'Dictionary_Users_' + item + '.txt', 'w') as f2:
		json.dump(reviewerIdUsers, f2)

if __name__ == '__main__':
	start_time = time.time()
	main(sys.argv)
	print 'Execution time is ' + str(time.time() - start_time) + ' seconds'
