import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import os

def read_csv(csv_path):
	lines = open(csv_path, 'r').readlines()
	hp_list = []
	ss_list = []
	for line in lines:
		parts = line.replace('\n', '').split(',')
		hp = float(parts[0])
		ss = float(parts[1])
		hp_list.append(hp)
		ss_list.append(ss)
	# hp_list = [x for x in hp_list if x > 0.5]
	# ss_list = [x for x in ss_list if x > 0.5]
	return hp_list, ss_list 

def plot_jasons_histogram(	l_1, l_2, output_png_path, ax, counter, subplot, colors,
							x_label='Predicted confidence', 
							y_label='Percent of Images', 
							num_bins=50,
							classes=['Hyperplastic']):
	

	if subplot is True:
		current = ax[counter][0]

		current.hist([l_1], num_bins, density=True, color=colors, label=classes)	

		# l_1 = list(sorted(l_1))
		# top_conf = l_1[int(len(l_1)/2):]
		# bott_conf = l_1[:int(len(l_1)/2)]
		# ax[counter].hist([top_conf, bott_conf], num_bins, density=True, color=colors, label=classes)

		current.set_xlabel(x_label, fontsize=24)
		current.set_ylabel(y_label, fontsize=24)
		# current.legend(prop={'size': 10})

		for tick in current.xaxis.get_major_ticks():
			tick.label.set_fontsize(20) 

		for tick in current.yaxis.get_major_ticks():
			tick.label.set_fontsize(20)
	else:
		ax.hist([l_1], num_bins, density=True, color=colors, label=classes)	

		ax.set_xlabel(x_label, fontsize=24)
		ax.set_ylabel(y_label, fontsize=24)
		# current.legend(prop={'size': 10})

		for tick in ax.xaxis.get_major_ticks():
			tick.label.set_fontsize(20) 

		for tick in ax.yaxis.get_major_ticks():
			tick.label.set_fontsize(20)


# def calculate_kl_divergence(easy_list, hard_list, num_bins):

# 	bins = np.arange(0, num_bins, 1) / num_bins

# 	easy_hist, _ = np.histogram(easy_list, bins, density = True)
# 	hard_hist, _ = np.histogram(hard_list, bins, density = True)

# 	print(easy_hist)
# 	print(hard_hist)
# 	kl_divergence = KL(easy_hist, hard_hist)

# 	print(kl_divergence, num_bins)


# def KL(P,Q):
# 	 epsilon = 0.00001

# 	 # You may want to instead make copies to avoid changing the np arrays.
# 	 P = P+epsilon
# 	 Q = Q+epsilon

# 	 divergence = np.sum(P*np.log(P/Q))
# 	 return divergence



if __name__ == "__main__":

	# easy_list = []
	# hard_list = []

	# model_paths = ['resnet18_e16_va0.768.pt', 'resnet18_e18_va0.793.pt', 'resnet18_e20_va0.798.pt', 'resnet18_e22_va0.813.pt'] # Manually input these
	# model_paths = ['resnet18_e26_va0.820.pt', 'resnet18_e28_va0.813.pt', 'resnet18_e30_va0.810.pt', 'resnet18_e32_va0.817.pt']
	model_paths = ['resnet18_e24_va0.816.pt']

	# test_paths = ['../models/hptohp_50/test/', '../models/hptohp_25/test/', '../models/hptohp_12/test/', '../models/hptohp_6/test/']
	# test_paths = ['../models/hptohp_50/datasets/EasyToHard/trainA/']
	test_paths = ['new_data/train_hp/easy/']

	fig, ax = plt.subplots(figsize = (7, 5))

	if len(test_paths) > 1:
		fig, ax = plt.subplots(len(test_paths), squeeze=False, figsize=(7, 20)) 

	plt.setp(ax, xlim=(0, 1), ylim=(0, 12))
	counter = 0

	# color_shades = [['navy'], ['blue'], ['cornflowerblue'], ['deepskyblue']]
	color_shades = [['forestgreen']]

	for i in range(len(test_paths)):
		path = test_paths[i]

		os.system('rm -r test/test/')
		os.system('cp -r ' + path + ' test/test/')

		all_hp = []
		all_ss = []

		csv_paths = []   # Will automatically be generated
		for each in model_paths:
			os.system("CVD=0 python code/filter.py --input_folder=test/ --top_image=0 --class_to_use=hp --output_folder=test/ --model_path=models/initial/" + each)
			csv_paths.append(each + "_confidences.csv")

		for each in csv_paths:
			hp_list, ss_list = read_csv(each)
			all_hp += hp_list
			all_ss += ss_list



		print("Average hyperplastic confidence: ", str(round(np.mean(all_hp), 3)))
		print("Standard deviation of hyperplastic confidences: ", str(round(np.std(all_ss), 3)))
		
		print("Compiling histogram for ", str(len(all_hp)), " confidences.")

		if len(test_paths) > 1:
			plot_jasons_histogram(all_hp, all_ss, 'confidence_histogram.png', ax, counter, True, color_shades[counter])
		else:
			plot_jasons_histogram(all_hp, all_ss, 'confidence_histogram.png', ax, counter, False, color_shades[counter])

		counter += 1

		# if i is 0:
		# 	easy_list = hp_list
		# elif i is 1:
		# 	hard_list = hp_list

	# for each in [2, 10, 50, 100]:
	# 	calculate_kl_divergence(easy_list, hard_list, each)

	plt.tight_layout(pad=3.0)
	plt.gcf().subplots_adjust(left=0.15)
	plt.savefig('confidence_histogram.png', dpi=400)











