import os
import cv2
import random
import argparse
import numpy as np
import csv
import skimage.measure
from scipy.misc import imsave
from Image_Class import Image_Class

parser = argparse.ArgumentParser()
parser.add_argument('--hp_folder_easy', type = str, help = "path to the folder with easy HP images")
parser.add_argument('--hp_folder_hard', type = str, help = "path to the folder with hard HP images")
parser.add_argument('--ss_folder', type = str, help = "path to the folder with SSA images")
parser.add_argument('--hp_folder_generated', type = str, help = "path to the folder with generated HP images")
args = parser.parse_args()

output_folder = 'turing_test/'

# Change number of images per class
num_hp_easy = 75
num_hp_hard = 75
num_hp_generated = 75
num_ss = 75

#Whether an image is whitespace, takes in np array
def is_whitespace(crop):
	pooled = skimage.measure.block_reduce(crop, (int(crop.shape[0]/10), int(crop.shape[1]/10), 3), np.average)
	pooled = np.mean(pooled, axis=2)
	pooled = np.rint(pooled[:9, :9])
	num_good_squares = 0
	for x in np.nditer(pooled):
		if x < 225: 
			num_good_squares += 1
	if num_good_squares > 70: 
		return False
	return True


def rotate_randomly(image_path):
	img = cv2.imread(image_path)
	b, g, r = cv2.split(img)
	img = cv2.merge((r, g, b))

	random_num = random.randint(1, 3)

	if random_num is 1:
		return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
	elif random_num is 2:
		return cv2.rotate(img, cv2.ROTATE_180)
	elif random_num is 3:
		return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)


#Returns a dictionary with new names like 1.jpg
def rename(shuffled_keys):
	#Create the dictionary
	result = {} 	#the key is real image name (e.g. "real/no_alk_123.jpg"), the value is the new name to use (e.g. 1.png)

	#Add to the dictionary
	counter = 0
	for key in shuffled_keys:
		counter+=1
		result[key] = str(counter)

	return result


#Returns a list of shuffled keys of a dictionary
def get_shuffled_keys(dictionary):
	keys = list(dictionary.keys())
	random.shuffle(keys)
	return keys


def generate_test(hp_folder_easy, hp_folder_generated, hp_folder_hard, ss_folder, num_hp_easy, num_hp_hard, num_hp_generated, num_ss):
	#Dictionaries to record data about each image
	class_dictionary = {}					#Key is image name (e.g. 'real/abc.jpg') and value is its class
	original_and_renamed_dictionary = {}	#Key is image name (e.g. 'real/abc.jpg') and value is the new anonymized name (e.g. '1.png')

	#Loop through generated HP images
	counter = 0
	images = os.listdir(hp_folder_generated)
	generated_images = []
	random.shuffle(images)
	for image in images:
		if counter < num_hp_generated:
			#Get image path
			image_path = os.path.join(hp_folder_generated, image)

			#Update dictionary
			class_dictionary[image_path] = "HP_Generated"

			generated_images.append(image_path)
			counter += 1
		else:
			break

	#Loop through easy HP images
	counter = 0
	images = os.listdir(hp_folder_easy)
	easy_images = []
	random.shuffle(images)
	for image in images:
		if counter < num_hp_easy and os.path.join(hp_folder_generated, 'AtoB_' + image) in generated_images:
			#Get image path
			image_path = os.path.join(hp_folder_easy, image)

			#Update dictionary
			class_dictionary[image_path] = "HP_Easy"

			easy_images.append(image)
			counter += 1

	#Get list of non-whitespace easy HP images that have not been picked yet
	non_whitespace_images = []
	for each in os.listdir(hp_folder_easy):
		if not is_whitespace(Image_Class(os.path.join(hp_folder_easy, each)).get_image()) and os.path.join(hp_folder_easy, each) not in class_dictionary:
			non_whitespace_images.append(each)

	#Delete and reacquire images until there are no images with whitespace
	for each in easy_images:
		if is_whitespace(Image_Class(os.path.join(hp_folder_easy, each)).get_image()):
			#Remove the real and generated versions of the image from dictionary
			print(os.path.join(hp_folder_easy, each)) 
			os.system('cp -r ' + os.path.join(hp_folder_easy, each) + ' ' + os.path.join('blahblahblah', each))
			class_dictionary.pop(os.path.join(hp_folder_easy, each))
			class_dictionary.pop(os.path.join(hp_folder_generated, 'AtoB_' + each))

			#Pick new image to replace this one
			for image in non_whitespace_images:
				if ('AtoB_' + image) in os.listdir(hp_folder_generated):
					print('Replaced with ', image)
					generated_image_path = os.path.join(hp_folder_generated, 'AtoB_' + image)
					easy_image_path = os.path.join(hp_folder_easy, image)

					class_dictionary[generated_image_path] = "HP_Generated"
					class_dictionary[easy_image_path] = "HP_Easy"

					non_whitespace_images.remove(image)
					break

	#Loop through hard HP images
	counter = 0
	images = os.listdir(hp_folder_hard)
	random.shuffle(images)
	for image in images:
		if counter < num_hp_hard:
			#Get image path
			image_path = os.path.join(hp_folder_hard, image)

			#Update dictionary
			class_dictionary[image_path] = "HP_Hard"

			counter += 1
		else:
			break

	#Loop through SSA images
	counter = 0
	images = os.listdir(ss_folder)
	random.shuffle(images)
	for image in images:
		if counter < num_ss:
			#Get image path
			image_path = os.path.join(ss_folder, image)

			#Update dictionary
			class_dictionary[image_path] = "SSA"

			counter += 1
		else:
			break

	#Verify class distribution
	counter = 0
	for each in ["HP_Generated", "HP_Easy", "HP_Hard", "SSA"]:
		for key in class_dictionary.keys():
			if class_dictionary.get(key) is each:
				counter += 1

		if counter is not num_hp_easy:
			print("Class distribution incorrect", counter, each)
			return
		else:
			counter = 0

	shuffled_keys = get_shuffled_keys(class_dictionary)

	original_and_renamed_dictionary = rename(shuffled_keys)

	#Write master CSV
	with open('master_file.csv', mode = 'w') as file:
		writer = csv.writer(file, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
		writer.writerow(['Original Image Name', 'New Image Name', 'Original Class'])

		for each in shuffled_keys:
			if '.DS_Store' not in each:
				writer.writerow([each, original_and_renamed_dictionary.get(each) + '.png', class_dictionary.get(each)])

	#Create output folder
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)
	else:
		os.system('rm -r ' + output_folder)
		os.makedirs(output_folder)

	#Write pathologist CSV
	with open('pathologist_file.csv', mode = 'w') as file:
		writer = csv.writer(file, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
		writer.writerow(['Image Name', 'Class (HP or SSA)', 'Notes'])

		for each in shuffled_keys:
			writer.writerow([original_and_renamed_dictionary.get(each) + '.png', '', ''])

	#Output images
	for each in shuffled_keys:
		if '.DS_Store' not in each:
			# print(each)
			if class_dictionary.get(each) is "HP_Generated":
				imsave(os.path.join(output_folder, original_and_renamed_dictionary.get(each) + '.png'), rotate_randomly(each))
			else:
				os.system('cp -r ' + each + ' ' + os.path.join(output_folder, original_and_renamed_dictionary.get(each) + '.png'))







#		MAIN		#
generate_test(args.hp_folder_easy, args.hp_folder_generated, args.hp_folder_hard, args.ss_folder, num_hp_easy, num_hp_hard, num_hp_generated, num_ss)











