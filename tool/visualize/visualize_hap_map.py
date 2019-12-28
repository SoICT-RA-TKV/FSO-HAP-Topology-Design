import json
import sys
from matplotlib import pyplot as plt

def main():
	hap_maps = sys.argv[1]
	maps = json.loads(open(hap_maps).read())
	HAPS = maps["HAP"]
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
		if len(c) == 0:
			print('0:', h)
		elif len(c) == 1:
			print('1:', h)
	plt.axis('scaled')
	plt.show()

if __name__ == "__main__":
	main()