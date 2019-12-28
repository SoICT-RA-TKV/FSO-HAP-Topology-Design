import json
import sys
from xalglib import *
from copy import deepcopy as cp
import numpy as np
import math
import os
import dict_txt

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

def clustering(fso_map_file, config_file = 'clustering.json'):
	config = json.loads(open(config_file).read())
	fso_map = dict_txt.fso_txt2dict(fso_map_file)
	points = []
	pid = []
	for fso in fso_map['FSO']:
		points.append([fso['r'], fso['c']])
		pid.append(fso['id'])
	NC = config['NC'] # Số dài thông trên mỗi HAP
	
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
		if max(cluster[:, 0]) <= config['D']:
			res = cp(rep)
			r_cluster = cp(cluster)
			r_clusterpoints = cp(clusterpoints)
			last = k - 1
		else:
			first = k + 1

	hap_map = dict()
	NHAP = hap_map['NHAP'] = int(0)
	hap_map['k-coefficient'] = 3.0
	hap_map['BER-limited'] = 0.001
	hap_map['HAP'] = []
	for i in range(res.k):
		# print(clusterpoints[i])
		if r_cluster[i, 1] > NC:
			tmp_points = [points[j] for j in r_clusterpoints[i]]
			tmp_pid = [pid[j] for j in r_clusterpoints[i]]
			clusterizersetpoints(s, tmp_points, 2)
			rep = clusterizerrunkmeans(s, math.ceil(NC / r_cluster[i, 1]))
			hap_map['NHAP'] += rep.k
			tmp_cluster, tmp_clusterpoints = cal_distance(rep, r_clusterpoints[i], tmp_pid)
			print(rep.k)
			print(tmp_cluster)
			print(tmp_clusterpoints)
			for tmp_i in range(rep.k):
				hap_map['HAP'].append(dict())
				hap_map['HAP'][NHAP]['coordinates'] = dict()
				hap_map['HAP'][NHAP]['coordinates']['r'] = rep.c[tmp_i][0]
				hap_map['HAP'][NHAP]['coordinates']['c'] = rep.c[tmp_i][1]
				hap_map['HAP'][NHAP]['coordinates']['c'] = 0.0
				hap_map['HAP'][NHAP]['diameter'] = tmp_cluster[tmp_i, 0]
				hap_map['HAP'][NHAP]['NFSO'] = int(tmp_cluster[tmp_i, 1])
				hap_map['HAP'][NHAP]['FSO'] = []
				for tmp_id in tmp_clusterpoints:
					tmp_fso = {'id': tmp_id, 'r': points[tmp_id][0], 'c': points[tmp_id][1], 'l': 0.0}
					hap_map['HAP'][NHAP]['FSO'].append(tmp_fso)
				NHAP += 1
		else:
			hap_map['HAP'].append(dict())
			hap_map['HAP'][NHAP]['coordinates'] = dict()
			hap_map['HAP'][NHAP]['coordinates']['r'] = res.c[i][0]
			hap_map['HAP'][NHAP]['coordinates']['c'] = res.c[i][1]
			hap_map['HAP'][NHAP]['coordinates']['l'] = 0.0
			hap_map['HAP'][NHAP]['diameter'] = r_cluster[i, 0]
			hap_map['HAP'][NHAP]['NFSO'] = int(r_cluster[i, 1])
			hap_map['HAP'][NHAP]['FSO'] = []
			for iid in r_clusterpoints[i]:
				tmp_fso = {'id': iid, 'r': points[iid][0], 'c': points[iid][1], 'l': 0.0}
				hap_map['HAP'][NHAP]['FSO'].append(tmp_fso)
			NHAP += 1
	hap_map['NHAP'] = int(NHAP)

	throughput = np.zeros((hap_map['NHAP'], hap_map['NHAP']))
	for i in range(hap_map['NHAP']):
		for j in range(hap_map['NHAP']):
			for pi in hap_map['HAP'][i]['FSO']:
				for pj in hap_map['HAP'][j]['FSO']:
					throughput[i, j] += fso_map['throughput'][pi['id']][pj['id']]

	hap_map['throughput'] = throughput.tolist()

	hap_map_file = fso_map_file.replace('ground_fso', 'clustering')
	dict_txt.hap_dict2txt(hap_map, hap_map_file)

def clustering_batch(fso_map_file = 'data', config_file = 'clustering.json'):
	if os.path.isfile(fso_map_file):
		if fso_map_file.split('/')[-1].find('ground_fso') == 0 and fso_map_file.split('.')[-1] == 'txt':
			print('Clustering {}'.format(fso_map_file))
			clustering(fso_map_file)
	else:
		for file in os.listdir(fso_map_file):
			clustering_batch(fso_map_file = fso_map_file + '/' + file)

def main():
	if len(sys.argv) > 1:
		clustering_batch(fso_map_file = sys.argv[1])
	else:
		clustering_batch()

if __name__ == '__main__':
	main()