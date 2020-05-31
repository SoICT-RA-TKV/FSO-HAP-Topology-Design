import json
import sys
from matplotlib import pyplot as plt
import dict_txt
import os

global prefix
global visualize_func

def visualize_density(file):
	if file.split('/')[-1] != 'density.txt':
		return
	stream = open(file, 'r')
	mapName = stream.readline().split(' ')[0].replace('\n', '')
	NMap = int(stream.readline())
	ratio = float(stream.readline())
	stream.readline()
	density = []
	while True:
		tmp = stream.readline().replace('\n', '').split(' ')
		try:
			density.append([float(i) for i in tmp])
		except:
			break
	Nr = len(density)
	Nc = len(density[0])

	plt.imshow(density, interpolation='nearest', cmap='coolwarm', vmin=0, vmax=1)
	plt.savefig(file.replace('txt', 'png'))
	plt.clf()


def visualize_fso(file):
	_map = dict_txt.fso_txt2dict(file)
	r = []
	c = []
	for fso in _map["FSO"]:
		r.append(fso["r"])
		c.append(fso["c"])
	plt.scatter(c, r, marker = '+')
	plt.axis('scaled')
	image_file = file.split('.')
	image_file[-1] = 'png'
	image_file = '.'.join(image_file)
	plt.savefig(image_file)
	plt.clf()

def visualize_hap(file):
	_map = dict_txt.hap_txt2dict(file)
	HAPS = _map["HAP"]
	for HAP in HAPS:
		h = HAP["coordinates"]
		r = []
		c = []
		for fso in HAP["FSO"]:
			r.append(fso["r"])
			c.append(fso["c"])
		for i in range(len(c)):
			plt.plot([h["c"], c[i]], [h["r"], r[i]], c = 'g')
		plt.scatter([h["c"]], [h["r"]], c = 'r')
		plt.scatter(c, r, c = 'b', marker = '+')
	plt.axis('scaled')
	image_file = file.split('.')
	image_file[-1] = 'png'
	image_file = '.'.join(image_file)
	plt.savefig(image_file)
	plt.clf()

def visualize_batch(file = 'data'):
	global prefix
	global visualize_func
	if os.path.isfile(file):
		for p in prefix:
			if file.split('/')[-1].find(p) == 0 and file.split('.')[-1] == 'txt':
				print('Visualizing {}'.format(file))
				visualize_func[p](file)
				break
	else:
		for f in os.listdir(file):
			visualize_batch(file = file + '/' + f)

def main():
	global prefix
	global visualize_func
	prefix = ['gfso', 'clustering', 'density']
	visualize_func = {
	'gfso': visualize_fso,
	'clustering': visualize_hap,
	'density': visualize_density
	}
	if len(sys.argv) > 1:
		visualize_batch(file = sys.argv[1])
	else:
		visualize_batch()

if __name__ == "__main__":
	main()