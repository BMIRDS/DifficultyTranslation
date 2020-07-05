import csv
import random
import os

# Collect list of distinct slide names with mappings to anonymized tile names
def create_image_dictionary(mapping_path):
	slide_names_to_image = {}

	with open(mapping_path, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
		i = 0

		for row in reader:
			if i is 0:
				i += 1
			else:
				slide_name = row[0].split("_")[2]
				anonymized_name = row[1].split("/")[1]

				if slide_name in slide_names_to_image:
					slide_names_to_image.get(slide_name).append(anonymized_name)
				else:
					new_list = []
					new_list.append(anonymized_name)
					slide_names_to_image[slide_name] = new_list

	return slide_names_to_image


# Collect list of anonymized tile names for hp for a pathologist
def get_hp_preds(classifications_path):
	result = []
	file = open(classifications_path, 'r')

	for line in file:
		result.append(line[:-1])

	file.close()
	return result


# Collect list of anonymized tile names with mappings to class
def get_hp_tiles(classifications_paths):
	all_preds = [] 	# Each index is a list of pathologist predictions
	result = [] 	# List of hp images that 2/3 pathologists agree

	for each in classifications_paths:
		all_preds.append(get_hp_preds(each))

	# Get HP images
	for image_name in all_preds[0]:
		if image_name in all_preds[1] or image_name in all_preds[2]:
			result.append(image_name)
	
	for image_name in all_preds[1]:
		if image_name in all_preds[2]:
			result.append(image_name)

	result = (set)(result)

	return result


# Split by slide
def split_slides(split, image_dictionary, hp_tiles):
	hp_train = []
	ss_train = []
	num_slides = (int)(split * len(image_dictionary.keys()))

	keys = list(image_dictionary.keys())
	random.shuffle(keys)

	counter = 0
	for key in keys:
		if counter < num_slides:

			anonymized_images = image_dictionary.get(key)

			for each in anonymized_images:

				if each in hp_tiles:
					hp_train.append(each)
				else:
					ss_train.append(each)

			counter += 1
		else:
			break

	return hp_train, ss_train


# Randomly split by slide for training and testing sets
def train_test_split(image_dictionary, hp_tiles):
	split = 0.7
	hp_train, ss_train = split_slides(split, image_dictionary, hp_tiles)

	while (len(hp_train) < 1400 or len(hp_train) > 1600) or (len(ss_train) < 500 or len(ss_train) > 700):
		if len(hp_train) > 1200 and len(ss_train) > 1200:
			split += 0.02
		elif len(hp_train) < 1000 and len(ss_train) < 1000:
			split -= 0.02

		print("Failed with lengths", len(hp_train), len(ss_train), "trying new split", split)

		hp_train, ss_train = split_slides(split, image_dictionary, hp_tiles)

	print("HP Train Set: ", str(len(hp_train)), "images")
	print("SSA Train Set: ", str(len(ss_train)), "images")

	# Get list of all tiles
	all_tiles = []
	for key in image_dictionary.keys():
		for each in image_dictionary.get(key):
			all_tiles.append(each)

	# Save images to respective folders
	for each in all_tiles:
		if each in hp_train:
			os.system("cp -r " + os.path.join(image_folder, each) + " train_hp/")
		elif each in ss_train:
			os.system("cp -r " + os.path.join(image_folder, each) + " train_ss/")
		else:
			if each in hp_tiles:
				os.system("cp -r " + os.path.join(image_folder, each) + " test_hp/")
			else:
				os.system("cp -r " + os.path.join(image_folder, each) + " test_ss/")


# Main
classifications_paths = ['arief_hp.txt', 'bing_hp.txt', 'carol_hp.txt']
image_folder=  "combined_patches_anonymized/"
mapping_path = "sensitive_mappings.csv"

image_dictionary = create_image_dictionary(mapping_path)
# print(image_dictionary.keys())
print("Created image dictionary")

hp_tiles = get_hp_tiles(classifications_paths)
# print(hp_tiles)
print("Retrieved hyperplastic tile labels")

train_test_split(image_dictionary, hp_tiles)










