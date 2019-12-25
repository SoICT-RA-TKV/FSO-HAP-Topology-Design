from datetime import datetime
from random import random
import json
import numpy as np
import os

def main():
	config = json.loads(open("config.json", "r").read())
	NCfg = len(config)
	for iCfg in range(NCfg):
		cfg = config[iCfg]
		NMaps = cfg["NMaps"]
		for iMaps in range(NMaps):
			gen_maps(cfg)

def cmp(p0, p1):
	if p0[0] == p1[0] and p0[1] == p1[1]:
		return 0
	return 1

def gen_maps(cfg = None):
	if cfg == None:
		return
	Nr = cfg["Nr"]
	Nc = cfg["Nc"]
	Np = cfg["NPivot"]
	pivot = cfg["pivot"]
	FSO = set()
	for ir in range(Nr):
		for ic in range(Nc):
			p0 = np.array([ir, ic])
			infP = np.zeros((Np,))
			for ip in range(Np):
				coor = pivot[ip]["coordinates"]
				p1 = np.array([coor["r"], coor["c"]])
				if cmp(p0, p1) == 0:
					infP[ip] = float("inf")
				else:
					infP[ip] = 1 / pow(np.linalg.norm(p0 - p1), pivot[ip]["influence"]["r"])
			infS = sum(infP)
			prob = 0
			if infS != float("inf"):
				for ip in range(Np):
					prob += pivot[ip]["influence"]["c"] * (infP[ip] / infS)
			else:
				for ip in range(Np):
					if infP[ip] == float("inf"):
						prob = pivot[ip]["influence"]["c"]
						break
			rand = random()
			print(ir, ic, rand, prob)
			if rand < prob / cfg["ratio"]:
				FSO.add((ir + random(), ic + random(), 0.0))
	maps = dict()
	maps["NFSO"] = len(FSO)
	maps["FSO"] = []
	for fso in FSO:
		maps["FSO"].append(dict())
		i = len(maps["FSO"]) - 1
		maps["FSO"][i]["r"] = fso[0]
		maps["FSO"][i]["c"] = fso[1]
		maps["FSO"][i]["l"] = fso[2]

	NFSO = len(FSO)
	FSO = list(FSO)
	throughput = np.zeros((NFSO, NFSO))
	for i in range(NFSO):
		for j in range(NFSO):
			if (i == j):
				throughput[i, j] = 0.0
			else:
				throughput[i, j] = random() * 1000 / np.linalg.norm(np.array(FSO[i]) - np.array(FSO[j]))

	maps["throughput"] = throughput.tolist()
	dtNow = str(datetime.now()).replace(' ', '_').replace(':', '_')
	try:
		os.makedirs("../maps/" + cfg["mapsName"])
	except:
		pass
	mapsFName = "../maps/" + cfg["mapsName"] + "/" + dtNow + ".json"
	mapsFile = open(mapsFName, "w")
	mapsFile.write(json.dumps(maps, indent=2, separators=(',', ': ')))


if __name__ == "__main__":
	main()