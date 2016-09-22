import os 
import shutil


inp_path = "/media/inno/01D04251141467101/WKData/clean"
out_path = "/media/inno/01D04251141467101/WKData/cleanPipeline"

dfolder = os.listdir(inp_path)
meta = open("meta/relevant_scc.txt").read().split("\n")
visited = {}
data = open("filesdata.txt").read().strip().split("\n")
for line in data:
	c = line.split("	") 
	if c[0] not in visited:
		visited[c[0]] = 1
		state = c[1]
		scc = c[2]
		lobs = c[3]

		if scc in meta:
			directory = out_path + "/" + scc.replace("/"," or ")
			if not os.path.exists(directory):
				os.makedirs(directory)

			if "/" in c[0]:
				fname = c[0].split("/")[1]
				year = c[0].split("/")[0]
				for each in dfolder:
					if fname in each and year in each and state in each:
						relevant_file = fname
						
						shutil.copy(inp_path + "/" + each, directory + "/" + each)

