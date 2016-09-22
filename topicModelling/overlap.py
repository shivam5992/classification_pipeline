data = open("Results/Results.txt").read()
sections = data.split("-------------------------------------------------")

mains = {}
for section in sections:
	section = section.split("\n")

	if "" in section:
		section = filter(lambda a: a != "", section)

	if section:
		section_name = section[0]
		if section_name not in mains:
			mains[section_name] = []

		for line in section:
			if "*" in line:

				wrds = line.split("+")
				wrds = [wrd.split("*")[1].strip() for wrd in wrds]
				mains[section_name].extend(wrds)

ma = {}
sets = []
for x,y in mains.iteritems():
	sets.append(set(y))

for x in sets:
	for each in x:
		if each not in ma:
			ma[each] = 0
		ma[each] += 1
import operator
sorted_x = sorted(ma.items(), key=operator.itemgetter(1), reverse = True)
for k in sorted_x:
	print k[0] + "\t" + str(k[1])