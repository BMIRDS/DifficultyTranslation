import csv
import os

def create_directory(new_folder):
	if not os.path.exists(new_folder):
		os.mkdir(new_folder)


# Collect list of anonymized tile names for hp for a pathologist
def get_hp_preds(classifications_path):
	result = []
	file = open(classifications_path, 'r')

	for line in file:
		result.append(line[:-1])

	file.close()
	return result


# Returns number of pathologists that listed that image as HP
def agreement(image_name, all_pathologist_preds):
	counter = 0
	for i in range(len(all_pathologist_preds)):
		if image_name in all_pathologist_preds[i]:
			counter += 1

	return counter


# Saves easy and hard images in separate folders
def separate_easy_hard(input_folder, classification_paths):
	
	image_names = []

	#Get list of image names
	for each in os.listdir(input_folder):
		image_names.append(each)


	all_pathologist_preds = [] # Each index is a list of pathologist predictions

	# Get pathologist predictions
	for each in classification_paths:
		all_pathologist_preds.append(get_hp_preds(each))

	# Create dictionary where key is image name and value is # of pathologists that listed image as HP
	image_dictionary = {}
	for each in image_names:
		image_dictionary[each] = agreement(each, all_pathologist_preds)

	# Save images
	keys = list(image_dictionary.keys())
	for key in keys:
		if image_dictionary.get(key) == 0:		# Easy SSA
			os.system("cp -r " + os.path.join(input_folder, key) + " ss_easy")
		elif image_dictionary.get(key) == 1: 	# Hard SSA
			os.system("cp -r " + os.path.join(input_folder, key) + " ss_hard")
		elif image_dictionary.get(key) == 2:	# Hard HP
			os.system("cp -r " + os.path.join(input_folder, key) + " hp_hard")
		elif image_dictionary.get(key) == 3:	# Easy HP
			os.system("cp -r " + os.path.join(input_folder, key) + " hp_easy")

# Main
classifications_paths = ['arief_hp.txt', 'bing_hp.txt', 'carol_hp.txt']
input_folder = 'new_data/train/ss/'
output_folders = ['ss_easy', 'ss_hard', 'hp_easy', 'hp_hard']

# Create output folder
for each in output_folders:
	create_directory(each)

separate_easy_hard(input_folder, classifications_paths)
