import json
import sys
from matplotlib import pyplot as plt

def main():
	fso_maps = sys.argv[1]
	maps = json.loads(open(fso_maps).read())
	r = []
	c = []
	for fso in maps["FSO"]:
		r.append(fso["r"])
		c.append(fso["c"])
	plt.scatter(c, r)
	plt.axis('scaled')
	plt.show()

if __name__ == "__main__":
	main()