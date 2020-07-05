import os
import sklearn
import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.manifold import TSNE
from numpy.random import seed
seed(0)
matplotlib.use('TkAgg')

def plot_tsne(confidences_easy, confidences_hard, confidences_gen, confidences_ss):
	y_pred = []
	test_y = []		# 0 - HP; 1 - SSA
	labels = []		# 0 - HP Easy; 1 - HP Hard; 2 - HP Generated; 3 - SSA

	for each in [confidences_easy, confidences_hard, confidences_gen]:
		lines = open(each, 'r').readlines()
		for line in lines:
			parts = line.replace('\n', '').split(',')
			y_pred.append(parts)
			test_y.append(0)

			if each is confidences_easy:
				labels.append(0)
			elif each is confidences_hard:
				labels.append(1)
			elif each is confidences_gen:
				labels.append(2)

	for each in [confidences_ss]:
		lines = open(each, 'r').readlines()
		for line in lines:
			parts = line.replace('\n', '').split(',')
			y_pred.append(parts)
			test_y.append(1)
			labels.append(3)

	print('Processed Confidences')

	Y = TSNE(n_components=2, perplexity=25, learning_rate=10, n_iter=5000).fit_transform(y_pred)

	print('Plotting TSNE...')

	#Create plot
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)


	# 4 classes
	classes = ['HP - Easy', 'HP - Hard', 'HP - Generated', 'SSA']
	colors = ['darkblue', 'blue', 'cornflowerblue', 'green']
	shapes = ['.']

	for i in range(len(labels)):
		label = labels[i]

		if label is 0:
			ax.scatter(Y[:, 0][i], Y[:, 1][i], c = colors[0], label = classes[0], marker = shapes[0])
		elif label is 1:
			ax.scatter(Y[:, 0][i], Y[:, 1][i], c = colors[1], label = classes[1], marker = shapes[0])
		elif label is 2:
			ax.scatter(Y[:, 0][i], Y[:, 1][i], c = colors[2], label = classes[2], marker = shapes[0])
		elif label is 3:
			ax.scatter(Y[:, 0][i], Y[:, 1][i], c = colors[3], label = classes[3], marker = shapes[0])

	#Custom colors
	handles = []
	for i in range(4):
		handles.append(matplotlib.lines.Line2D([], [], linewidth=0, color = colors[i], label = classes[i], marker = shapes[0]))

	#Resize plot
	plt.tight_layout()

	#Create legend with black border
	plt.legend(handles=handles, handlelength=1, handleheight=1, loc = 'upper right', 
		        prop={'size': 8, 'family':'Calibri'}).get_frame().set_edgecolor('black')

	plt.tick_params(axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False)
	plt.tick_params(axis = 'y', which = 'both', left = False, right = False, labelleft = False)
	#Rescale plot
	# ax.set_aspect(.04)
	#Final resizing and save image
	# plt.gcf().subplots_adjust(right=0.15)
	plt.savefig('TSNE.png', dpi=400, format = 'png')



# Main #
confidences_easy = 'confidences_hidden_layer/easy_confidences.csv'
confidences_hard = 'confidences_hidden_layer/hard_confidences.csv'
confidences_gen = 'confidences_hidden_layer/gen_confidences.csv'
confidences_ss = 'confidences_hidden_layer/ss_confidences.csv'

plot_tsne(confidences_easy, confidences_hard, confidences_gen, confidences_ss)







