import os
import numpy as np
import scipy.stats as st
import torch
import torch.nn as nn
from os.path import join, isfile, isdir
from os import listdir
from torchvision import datasets, models, transforms


#Returns the classes - input folder should have subfolders of classes
def get_classes(input_folder):
	result = []
	for each in os.listdir(input_folder):
		if each != ".DS_Store":
			result.append(each)
		else:
			os.remove(".DS_Store")
	return result


#getting the classes for classification
def get_classes(folder):
	subfolder_paths = sorted([f for f in listdir(folder) if (isdir(join(folder, f)) and '.DS_Store' not in f)])
	return subfolder_paths


#Gets confidence interval
def get_confidence_interval(class_accuracies, confidence):
	print(st.t.interval(.95, len(class_accuracies)-1, loc=np.mean(class_accuracies), scale=st.sem(class_accuracies)))


def get_accuracy(model, input_folder):

	#Set device for CUDA
	device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") 

	#Get classes
	classes = get_classes(input_folder)

	#Load in the model
	active_model = torch.load(model)
	active_model.train(False)
	print("Loaded the model")

	#dictionary - key: class, value: [correct, total]
	counters = {}
	for tissue_class in classes:
		counters[tissue_class] = [0, 0]

	class_num_to_class = {i:get_classes("../../../jason/cp_clean/train_folder/train/")[i] for i in range(len(get_classes("../../../jason/cp_clean/train_folder/train/")))} 

	#data transforms, no augmentation this time.
	data_transforms = {
		'normalize': transforms.Compose([
	        transforms.CenterCrop(224),
	        transforms.ToTensor(),
	        transforms.Normalize([0.7, 0.6, 0.7], [0.15, 0.15, 0.15])
	    ]),
	    'unnormalize': transforms.Compose([
	        transforms.Normalize([1/0.15, 1/0.15, 1/0.15], [1/0.15, 1/0.15, 1/0.15])
	    ]),
	}

	#Begin processing the model's predictions, prints individaul class accuracy
	for tissue_class in os.listdir(input_folder):

		#Correctness list
		correctness = []

		#Safety check
		if tissue_class == ".DS_Store":
			continue

		image_dataset = datasets.ImageFolder(os.path.join(input_folder, tissue_class), data_transforms['normalize']) # May cause errors
		dataloader = torch.utils.data.DataLoader(image_dataset, batch_size=16, shuffle=False, num_workers=4)
		num_test_images = len(dataloader)*16

		for test_inputs, test_labels in dataloader:

			#Model predictions
			test_inputs = test_inputs.to(device)
			test_outputs = active_model(test_inputs)
			softmax_test_outputs = nn.Softmax()(test_outputs)
			confidences, test_preds = torch.max(softmax_test_outputs, 1)

			for i in range(test_preds.shape[0]):
				confidence = confidences[i].data.item()
				predicted_class = class_num_to_class[test_preds[i].data.item()]

				if predicted_class == tissue_class:
					counters[tissue_class] = (counters.get(tissue_class)[0]+1, counters.get(tissue_class)[1])
					correctness.append(1)
				else:
					correctness.append(0)
				
				counters[tissue_class] = [counters.get(tissue_class)[0], counters.get(tissue_class)[1]+1]

		print(tissue_class + ": " + str(round(1.0*counters.get(tissue_class)[0]/counters.get(tissue_class)[1], 3)))
		get_confidence_interval(correctness, .95)	

	#Combined class accuracy
	correct, total = 0, 0
	for key, value in counters.items():
		correct += value[0]
		total += value[1]
	print("Combined: " + str(round(1.0*correct/total, 3)))

	#Grab a confidence interval
	class_accuracies = []
	for key, value in counters.items():
		class_accuracies.append(1.0*value[0]/value[1])
	get_confidence_interval(class_accuracies, .95)




#	MAIN	#
model_path = "resnet18_e11_va0.860.pt"
folder_to_test_on = "val"

get_accuracy(model_path, folder_to_test_on)



















