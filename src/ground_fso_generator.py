from datetime import datetime
from random import random
import json
import numpy as np
import os
import dict_txt
from utils import *
import sys

def main():
	if len(sys.argv) > 1:
		cal_density_batch(file = sys.argv[1])
	else:
		cal_density_batch()
	if len(sys.argv) > 1:
		file = sys.argv[1]
		if len(sys.argv) > 2:
			file = sys.argv[2]
		ground_fso_generate_batch(file = file)
	else:
		ground_fso_generate_batch()

def cal_density(file):
	if file.split('/')[-1] != 'config.txt':
		return
	cfg = dict_txt.config_ground_fso_txt2dict(file)
	print('Calculating density of configuration {}'.format(cfg['mapName']))
	Nr = cfg['Nr']
	Nc = cfg['Nc']
	Np = cfg['NPivot']
	pivot = cfg['pivot']
	density = []
	for ir in range(Nr):
		density.append([])
		for ic in range(Nc):
			p0 = np.array([ir, ic])
			infP = np.zeros((Np,))
			for ip in range(Np):
				coordinates = pivot[ip]['coordinates']
				p1 = np.array([coordinates['r'], coordinates['c']])
				if cmp(p0, p1) == 0:
					infP[ip] = float('inf')
				else:
					infP[ip] = 1 / pow(np.linalg.norm(p0 - p1), pivot[ip]['influence']['r'])
			infS = sum(infP)
			prob = 0
			if infS != float('inf'):
				for ip in range(Np):
					prob += pivot[ip]['influence']['c'] * (infP[ip] / infS)
			else:
				for ip in range(Np):
					if infP[ip] == float('inf'):
						prob = pivot[ip]['influence']['c']
						break
			density[ir].append(prob)
	stream = open(file.replace('config.txt', 'density.txt'), 'w')
	stream.write(cfg['mapName'] + '\n')
	stream.write(str(cfg['NMap']) + '\n')
	stream.write(str(cfg['ratio']) + '\n')
	for ir in range(Nr):
		stream.write(join_any(' ', density[ir]) + '\n')

def cal_density_batch(file = 'data'):
	if os.path.isfile(file):
		if file.split('/')[-1] == 'config.txt':
			cal_density(file)
	else:
		for f in os.listdir(file):
			cal_density_batch(file = file + '/' + f)

def ground_fso_generate_batch(file = 'data'):
	if os.path.isfile(file):
		if file.split('/')[-1] == 'density.txt':
			ground_fso_generate(file)
	else:
		for f in os.listdir(file):
			ground_fso_generate_batch(file = file + '/' + f)

def cmp(p0, p1):
	if p0[0] == p1[0] and p0[1] == p1[1]:
		return 0
	return 1

def ground_fso_generate(file = 'density.txt'):
	if file.split('/')[-1] != 'density.txt':
		return
	stream = open(file, 'r')
	mapName = stream.readline().split(' ')[0].replace('\n', '')
	NMap = int(stream.readline())
	ratio = float(stream.readline())
	density = []
	while True:
		tmp = stream.readline().replace('\n', '').split(' ')
		try:
			density.append([float(i) for i in tmp])
		except:
			break
	Nr = len(density)
	Nc = len(density[0])
	for i in range(NMap):
		print('Generating map {} {}'.format(mapName, i))
		FSO = set()
		for ir in range(Nr):
			for ic in range(Nc):
				prob = density[ir][ic]
				rand = random()
				if rand < prob / ratio:
					FSO.add((ir + random(), ic + random(), 0.0))
		_map = dict()
		_map['NFSO'] = len(FSO)
		_map['FSO'] = []
		for fso in FSO:
			_map['FSO'].append(dict())
			i = len(_map['FSO']) - 1
			_map['FSO'][i]['id'] = i
			_map['FSO'][i]['r'] = fso[0]
			_map['FSO'][i]['c'] = fso[1]
			_map['FSO'][i]['l'] = fso[2]
		NFSO = len(FSO)
		FSO = list(FSO)
		throughput = np.zeros((NFSO, NFSO), dtype = int)
		for i in range(NFSO):
			for j in range(NFSO):
				if (i == j):
					throughput[i, j] = 0.0
				else:
					throughput[i, j] = random() * Nr * Nc / np.linalg.norm(np.array(FSO[i]) - np.array(FSO[j]))
		_map['throughput'] = throughput.tolist()
		dtNow = str(datetime.now()).replace(' ', '_').replace(':', '_')
		try:
			os.makedirs('./data/' + mapName)
		except:
			pass
		mapFName = './data/' + mapName + '/' + 'ground_fso_' + mapName + '_' + dtNow + '.txt'
		dict_txt.fso_dict2txt(data = _map, file = mapFName)


if __name__ == '__main__':
	main()