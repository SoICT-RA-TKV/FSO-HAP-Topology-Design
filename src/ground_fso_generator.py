from datetime import datetime
from random import random
import json
import numpy as np
import os
import dict_txt

def main():
	config = json.loads(open('ground_fso_generator.json', 'r').read())
	NCfg = len(config)
	for iCfg in range(NCfg):
		cfg = config[iCfg]
		NMap = cfg['NMap']
		for iMap in range(NMap):
			ground_fso_generator(cfg)
			print('Generated map {} {}'.format(cfg['mapName'], iMap))

def cmp(p0, p1):
	if p0[0] == p1[0] and p0[1] == p1[1]:
		return 0
	return 1

def ground_fso_generator(cfg = None):
	if cfg == None:
		return
	Nr = cfg['Nr']
	Nc = cfg['Nc']
	Np = cfg['NPivot']
	pivot = cfg['pivot']
	FSO = set()
	for ir in range(Nr):
		for ic in range(Nc):
			p0 = np.array([ir, ic])
			infP = np.zeros((Np,))
			for ip in range(Np):
				coor = pivot[ip]['coordinates']
				p1 = np.array([coor['r'], coor['c']])
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
			rand = random()
			if rand < prob / cfg['ratio']:
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
	throughput = np.zeros((NFSO, NFSO))
	for i in range(NFSO):
		for j in range(NFSO):
			if (i == j):
				throughput[i, j] = 0.0
			else:
				throughput[i, j] = random() * Nr * Nc / np.linalg.norm(np.array(FSO[i]) - np.array(FSO[j]))
	_map['throughput'] = throughput.tolist()
	dtNow = str(datetime.now()).replace(' ', '_').replace(':', '_')
	try:
		os.makedirs('./data/' + cfg['mapName'])
	except:
		pass
	mapFName = './data/' + cfg['mapName'] + '/' + 'ground_fso_' + cfg['mapName'] + '_' + dtNow + '.txt'
	dict_txt.fso_dict2txt(data = _map, file = mapFName)


if __name__ == '__main__':
	main()