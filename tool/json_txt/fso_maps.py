import json
import sys
import numpy as np

def join_any(s, arr):
	for i in range(len(arr)):
		arr[i] = str(arr[i])
	return s.join(arr)

def json2txt(json_file, txt_file = None):
	if txt_file == None:
		tmp = json_file.split('.')
		if tmp[-1] == 'json':
			tmp[-1] = 'txt'
		else:
			tmp.append('txt')
		txt_file = '.'.join(tmp)
	json_read_stream = open(json_file, "r")
	txt_write_stream = open(txt_file, "w")

	fso_maps = json.loads(json_read_stream.read())

	NFSO = fso_maps["NFSO"]
	FSO = fso_maps["FSO"]
	bw = fso_maps["throughput"]

	txt_write_stream.write(str(NFSO) + "\n")

	for i in range(NFSO):
		txt_write_stream.write(join_any(' ', [FSO[i]["r"], FSO[i]["c"], FSO[i]["l"]]) + "\n")

	for i in range(NFSO):
		for j in range(NFSO):
			txt_write_stream.write(join_any(' ', [i, j, bw[i][j]]) + "\n")

def txt2json(txt_file, json_file = None):
	if json_file == None:
		tmp = txt_file.split('.')
		if tmp[-1] == 'txt':
			tmp[-1] = 'json'
		else:
			tmp.append('json')
	json_write_stream = open(json_file, "w")
	txt_read_stream = open(txt_file, "r")

	fso_maps = dict()
	NFSO = fso_maps["NFSO"] = int(txt_read_stream.readline())
	FSO = fso_maps["FSO"] = []
	for i in range(NFSO):
		tmp = [float(t) for t in txt_read_stream.readline().split(' ')]
		tmp_d = dict()
		tmp_d["id"] = i
		tmp_d["r"], tmp_d["c"], tmp_d["l"]  = tmp[:3]
		FSO.append(tmp_d)

	bw = np.zeros((NFSO, NFSO))
	while True:
		a = txt_read_stream.readline().split(' ')
		if len(a) != 3:
			break
		bw[int(a[0]), int(a[1])] = float(a[2])

	fso_maps["throughput"] = bw.tolist()

	json_write_stream.write(json.dumps(fso_maps, indent = 2, separators=(',', ': ')))

if __name__ == "__main__":
	input_file = sys.argv[1]
	output_file = None
	if len(sys.argv) > 3:
		output_file = sys.argv[2]
	f = sys.argv[-1]
	if f == "json2txt":
		json2txt(json_file = input_file, txt_file = output_file)
	elif f == "txt2json":
		txt2json(txt_file = input_file, json_file = output_file)