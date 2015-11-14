from sys import argv
import gzip
import shutil
import pickle
import json
from matplotlib import pyplot

script, directory, directoryReviews, item, year = argv

newEdges = {} # Ground truth next year

def parseIterator(path):
	g = gzip.open(path, 'r')
	for l in g:
		yield eval(l)

def findNewEdges():
	with open(directory + 'Dictionary_Items_' + item + '.txt', 'r') as f1:
		asinItems = json.load(f1)
	with open(directory + 'Dictionary_Users_' + item + '.txt', 'r') as f2:
		reviewerIdUsers = json.load(f2)
	with open(directoryReviews + 'reviews_' + item + '_' + year + '.json', 'rb') as f_in, gzip.open(directoryReviews + 'reviews_' + item + '_' + year + '.json.gz', 'wb') as f_out:
		shutil.copyfileobj(f_in, f_out)
	for review in parseIterator(directoryReviews + 'reviews_' + item + '_' + year + '.json.gz'):
		queryUser = review['reviewerID']
		if queryUser in reviewerIdUsers: # Check if user in the years we predicted from
			if not queryUser in newEdges:
				newEdges[queryUser] = []
			newEdges[queryUser].append(asinItems[review['asin']])

def checkEdges():
	with open(directory + 'recommendations','rb') as f:
		predictions = pickle.load(f)

	allScores = []
	allPreds = []
	for cluster in range(0, len(predictions)):
		commScores = []
		commPreds = []
		for user, items in predictions[cluster].iteritems():
			if not user in newEdges:
				groundTruth = set()
			else:
				groundTruth = set(newEdges[user])
			itemSet = set(items)
			matched = set.intersection(*[itemSet, groundTruth])
			if len(itemSet) == 0:
				score = 0.5
				continue
			else:
				score = len(matched)*1.0/len(itemSet)
			commScores.append(score)
			commPreds.append(len(itemSet))
		allScores.append(commScores)
		allPreds.append(commPreds)
	
	commScores = [sum(x)*100.0/(0.000001+len(x)) for x in allScores]
	commPreds = [sum(x)/(0.000001+len(x)) for x in allPreds]
	print zip(commScores, commPreds)
	pyplot.plot(range(len(predictions)), commScores, 'b-', label = 'Correct')
	#pyplot.plot(range(len(predictions)), commPreds, 'r--', label = 'Correct')
	pyplot.title('Cluster vs. Percentage of Predictions')
	pyplot.xlabel('Cluster')
	pyplot.ylabel('Percentage of Correct Predictions')
	pyplot.legend(loc = 'upper right')
	pyplot.show()

def main(argv):
	findNewEdges()
	checkEdges()

if __name__ == '__main__':
	main(argv)