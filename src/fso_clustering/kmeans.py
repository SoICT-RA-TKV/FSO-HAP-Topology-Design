import json
import sys
from xalglib import *
from copy import deepcopy as cp
import numpy as np
import math

def cal_distance(rep, points, pid):
	cluster = np.zeros((rep.k, 2))
	clusterpoints = []
	for i in range(rep.k):
		clusterpoints.append([])
	for j in range(rep.npoints):
		i = rep.cidx[j]
		distance = np.linalg.norm(np.array(rep.c[i]) - np.array(points[j]))
		cluster[i, 0] = max(cluster[i, 0], distance) # Cluster diameter
		cluster[i, 1] += 1 # Number of FSO in cluster
		clusterpoints[i].append(pid[j]) # List of FSO id in cluster
	return cluster, clusterpoints

def main():
	config = json.loads(open("config.json").read())
	fso_maps = json.loads(open(sys.argv[1]).read())

	points = []
	pid = []
	for fso in fso_maps["FSO"]:
		points.append([fso["r"], fso["c"]])
		pid.append(fso["id"])

	NC = config["NC"] # Số dài thông trên mỗi HAP

	s = clusterizercreate()
	clusterizersetpoints(s, points, 2)
	clusterizersetkmeanslimits(s, 100, 0)

	first = math.ceil(len(points) / NC)
	last = len(points)
	r_cluster = None
	r_clusterpoints = None
	while first <= last:
		k = int((first + last) / 2)
		rep = clusterizerrunkmeans(s, k)
		cluster, clusterpoints = cal_distance(rep, points, pid)
		if max(cluster[:, 0]) <= config["D"]:
			res = cp(rep)
			r_cluster = cp(cluster)
			r_clusterpoints = cp(clusterpoints)
			last = k - 1
		else:
			first = k + 1

	hap_maps = dict()
	NHAP = hap_maps["NHAP"] = int(0)
	hap_maps["k-coefficient"] = 3.0
	hap_maps["BER-limited"] = 0.001
	hap_maps["HAP"] = []
	for i in range(res.k):
		# print(clusterpoints[i])
		if r_cluster[i, 1] > NC:
			tmp_points = [points[j] for j in r_clusterpoints[i]]
			tmp_pid = [pid[j] for j in r_clusterpoints[i]]
			clusterizersetpoints(s, tmp_points, 2)
			rep = clusterizerrunkmeans(s, math.ceil(NC / r_cluster[i, 1]))
			hap_maps["NHAP"] += rep.k
			tmp_cluster, tmp_clusterpoints = cal_distance(rep, r_clusterpoints[i], tmp_pid)
			print(rep.k)
			print(tmp_cluster)
			print(tmp_clusterpoints)
			for tmp_i in range(rep.k):
				hap_maps["HAP"].append(dict())
				hap_maps["HAP"][NHAP]["coordinates"] = dict()
				hap_maps["HAP"][NHAP]["coordinates"]["r"] = rep.c[tmp_i][0]
				hap_maps["HAP"][NHAP]["coordinates"]["c"] = rep.c[tmp_i][1]
				hap_maps["HAP"][NHAP]["diameter"] = tmp_cluster[tmp_i, 0]
				hap_maps["HAP"][NHAP]["NFSO"] = int(tmp_cluster[tmp_i, 1])
				hap_maps["HAP"][NHAP]["FSO"] = []
				for tmp_id in tmp_clusterpoints:
					hap_maps["HAP"][NHAP]["FSO"].append({"id": tmp_id, "r": points[tmp_id][0], "c": points[tmp_id][1]})
				NHAP += 1
		else:
			hap_maps["HAP"].append(dict())
			hap_maps["HAP"][NHAP]["coordinates"] = dict()
			hap_maps["HAP"][NHAP]["coordinates"]["r"] = res.c[i][0]
			hap_maps["HAP"][NHAP]["coordinates"]["c"] = res.c[i][1]
			hap_maps["HAP"][NHAP]["diameter"] = r_cluster[i, 0]
			hap_maps["HAP"][NHAP]["NFSO"] = int(r_cluster[i, 1])
			hap_maps["HAP"][NHAP]["FSO"] = []
			for iid in r_clusterpoints[i]:
				hap_maps["HAP"][NHAP]["FSO"].append(dict({"id": iid, "r": points[iid][0], "c": points[iid][1]}))
			NHAP += 1
	hap_maps["NHAP"] = int(NHAP)

	bw = np.zeros((hap_maps["NHAP"], hap_maps["NHAP"]))
	for i in range(hap_maps["NHAP"]):
		for j in range(hap_maps["NHAP"]):
			for pi in hap_maps["HAP"][i]["FSO"]:
				for pj in hap_maps["HAP"][j]["FSO"]:
					bw[i, j] += fso_maps["throughput"][pi["id"]][pj["id"]]

	hap_maps["throughput"] = bw.tolist()


	open("res.json", "w").write(json.dumps(hap_maps, indent=2, separators=(',', ': ')))

	
if __name__ == "__main__":
	main()