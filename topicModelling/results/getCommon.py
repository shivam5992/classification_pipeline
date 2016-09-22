from textblob import TextBlob

data = open("100words.txt").read().split("\n")
# class Common:
# 	def intersect(*d):
# 	    sets = iter(map(set, d))
# 	    result = sets.next()
# 	    for s in sets:
# 	        result = result.intersection(s)
# 	    return result

# 	mains = {}
# 	for line in data:
# 		wrd = line.split("	")[0]
# 		cat = line.split("	")[2]

# 		if cat not in mains:
# 			mains[cat] = []
# 		mains[cat].append(wrd)


# 	counts = {}
# 	for k, y in mains.iteritems():
# 		for each in list(set(y)):
# 			if each not in counts:
# 				counts[each] = 0
# 			counts[each] += 1


# 	for k,y in counts.iteritems():
# 		if y == 10:
# 			print k 

# class POS:
for line in data:
	wrd = line.split("	")[0]
	freq = line.split("	")[1]
	cat = line.split("	")[2]
	tag = TextBlob(wrd).tags[0][1]

	print line + "	" + tag