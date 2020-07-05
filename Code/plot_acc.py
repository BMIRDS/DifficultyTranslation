input_folder = '../../../jason/polyp/checkpoints_5/'

import os
import csv

with open('val_acc.csv', mode = 'w') as file:
	writer = csv.writer(file, delimiter = ',', quoting = csv.QUOTE_MINIMAL)

	for model_name in os.listdir(input_folder):

		epoch = model_name.split('_')[1][1:]
		acc = (int)(model_name.split('.')[1])/1000

		writer.writerow([epoch, (str)(acc)])

