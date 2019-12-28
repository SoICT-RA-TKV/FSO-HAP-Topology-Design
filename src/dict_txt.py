import json
import sys
import numpy as np

def join_any(separator, data):
	for i in range(len(data)):
		data[i] = str(data[i])
	return separator.join(data)

def fso_dict2txt(data, file):
	stream = open(file, 'w')
	NFSO = data['NFSO']
	FSO = data['FSO']
	throughput = data['throughput']
	stream.write('#So luong nut la la\n')
	stream.write(str(NFSO) + '\n')
	stream.write('#Toa do cac nut\n')
	for i in range(NFSO):
		stream.write(join_any(' ', [FSO[i]['r'], FSO[i]['c'], FSO[i]['l']]) + '\n')
	stream.write('#Ma tran yeu cau D\n')
	stream.write('#source_index dest_index bw don vi Mbps\n')
	for i in range(NFSO):
		for j in range(NFSO):
			stream.write(join_any(' ', [i, j, throughput[i][j]]) + '\n')

def fso_txt2dict(file):
	stream = open(file, 'r')
	data = dict()
	stream.readline()
	NFSO = data['NFSO'] = int(stream.readline())
	stream.readline()
	FSO = data['FSO'] = []
	for i in range(NFSO):
		tmp = [float(t) for t in stream.readline().split(' ')]
		tmp_d = dict()
		tmp_d['id'] = i
		tmp_d['r'], tmp_d['c'], tmp_d['l']  = tmp[:3]
		FSO.append(tmp_d)
	throughput = np.zeros((NFSO, NFSO), dtype = int)
	stream.readline()
	stream.readline()
	while True:
		a = stream.readline().split(' ')
		if len(a) != 3:
			break
		throughput[int(a[0]), int(a[1])] = int(a[2])
	data['throughput'] = throughput.tolist()
	return data

def hap_dict2txt(data, file):
	stream = open(file, 'w')
	NHAP = data['NHAP']
	HAP = data['HAP']
	throughput = data['throughput']
	stream.write('#He so k la\n')
	stream.write(str(data['k-coefficient']) + '\n')
	stream.write('#Number of Nodes\n')
	stream.write(str(NHAP) + '\n')
	stream.write('# list of nodes\n')
	stream.write('#x #y #z\n')
	for i in range(NHAP):
		tmp_hap = HAP[i]['coordinates']
		stream.write(join_any(' ', [tmp_hap['r'], tmp_hap['c'], tmp_hap['l']]) + '\n')
	stream.write('#nguong BER\n')
	stream.write(str(data['BER-limited']) + '\n')
	stream.write('#Ma tran yeu cau D\n')
	stream.write('#source_index dest_index bw don vi Mbps\n')
	for i in range(NHAP):
		for j in range(NHAP):
			stream.write(join_any(' ', [i, j, throughput[i][j]]) + '\n')
	stream.write('#Chi tiet cac cum\n')
	for i in range(NHAP):
		stream.write(str(HAP[i]['diameter']) + '\n')
		tmp_nfso = HAP[i]['NFSO']
		stream.write(str(tmp_nfso) + '\n')
		for j in range(tmp_nfso):
			tmp_fso = HAP[i]['FSO'][j]
			tmp_data = [tmp_fso['id'], tmp_fso['r'], tmp_fso['c'], tmp_fso['l']]
			stream.write(join_any(' ', tmp_data) + '\n')


def hap_txt2dict(file):
	stream = open(file, 'r')
	data = dict()
	stream.readline()
	data['k-coefficient'] = float(stream.readline())
	stream.readline()
	NHAP = data['NHAP'] = int(stream.readline())
	stream.readline()
	stream.readline()
	HAP = data['HAP'] = []
	throughput = np.zeros((NHAP, NHAP), dtype = int)
	a = None
	for i in range(NHAP):
		tmp = [float(t) for t in stream.readline().split(' ')]
		tmp_d = dict()
		tmp_d['r'], tmp_d['c'], tmp_d['l']  = tmp[:3]
		tmp = {'coordinates': tmp_d}
		HAP.append(tmp)
	stream.readline()
	data['BER-limited'] = float(stream.readline())
	stream.readline()
	stream.readline()
	while True:
		a = stream.readline()
		if a[0] == '#':
			break
		a = a.split(' ')
		throughput[int(a[0]), int(a[1])] = int(a[2])
	data['throughput'] = throughput.tolist()
	for i in range(NHAP):
		HAP[i]['diameter'] = float(stream.readline())
		tmp_mfso = HAP[i]['NFSO'] = int(stream.readline())
		FSO = HAP[i]['FSO'] = []
		for j in range(tmp_mfso):
			tmp_fso = stream.readline().split(' ')
			FSO.append(dict())
			FSO[j]['id'] = int(tmp_fso[0])
			FSO[j]['r'] = float(tmp_fso[1])
			FSO[j]['c'] = float(tmp_fso[2])
			FSO[j]['l'] = float(tmp_fso[3])
	return data

if __name__ == '__main__':
	pass