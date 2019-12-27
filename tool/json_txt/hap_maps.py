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

	hap_maps = json.loads(json_read_stream.read())

	txt_write_stream.write(str(hap_maps["k-coefficient"]) + "\n")

	NHAP = hap_maps["NHAP"]
	HAP = hap_maps["HAP"]
	bw = hap_maps["throughput"]
	txt_write_stream.write(str(NHAP) + "\n")

	for i in range(NHAP):
		tmp_hap = HAP[i]["coordinates"]
		txt_write_stream.write(join_any(' ', [tmp_hap["r"], tmp_hap["c"], tmp_hap["l"]]) + '\n')

	txt_write_stream.write(str(hap_maps["BER-limited"]) + '\n')

	for i in range(NHAP):
		for j in range(NHAP):
			txt_write_stream.write(join_any(' ', [i, j, bw[i][j]]) + '\n')

def txt2json(txt_file, json_file = None):
	if json_file == None:
		tmp = txt_file.split('.')
		if tmp[-1] == 'txt':
			tmp[-1] = 'json'
		else:
			tmp.append('json')
	json_write_stream = open(json_file, "w")
	txt_read_stream = open(txt_file, "r")

	hap_maps = dict()
	hap_maps["k-coefficient"] = float(txt_read_stream.readline())
	NHAP = hap_maps["NHAP"] = int(txt_read_stream.readline())
	HAP = hap_maps["HAP"] = []

	bw = np.zeros((NHAP, NHAP))
	a = None
	for i in range(NHAP):
		tmp = [float(t) for t in txt_read_stream.readline().split(' ')]
		tmp_d = dict()
		tmp_d["id"] = i
		tmp_d["r"], tmp_d["c"], tmp_d["l"]  = tmp[:3]
		HAP.append(tmp_d)


	hap_maps["BER-limited"] = float(txt_read_stream.readline())

	while True:
		a = txt_read_stream.readline().split(' ')
		if len(a) != 3:
			break
		bw[int(a[0]), int(a[1])] = float(a[2])

	hap_maps["throughput"] = bw.tolist()

	json_write_stream.write(json.dumps(hap_maps, indent = 2, separators=(',', ': ')))


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