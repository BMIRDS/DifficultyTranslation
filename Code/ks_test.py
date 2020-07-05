from scipy.stats import ks_2samp

def get_confidences(input_csv):
	lines = open(input_csv, 'r').readlines()
	hp_list = []
	ss_list = []
	for line in lines:
		parts = line.replace('\n', '').split(',')
		hp = float(parts[1])
		ss = float(parts[0])
		hp_list.append(hp)
		ss_list.append(ss)

	return hp_list


print(ks_2samp(get_confidences('easy_confidences.csv'), get_confidences('hard_confidences.csv')))