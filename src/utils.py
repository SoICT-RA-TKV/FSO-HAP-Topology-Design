

def process_batch(process_function, item = 'data'):
	if os.path.isfile(item):
		process_function(item)
	else:
		for sub in os.listdir(item):
			cal_density_batch(item = item + '/' + sub, process_function = process_function)

def join_any(separator, data):
    for i in range(len(data)):
    	data[i] = str(data[i])
    return ' '.join(data)