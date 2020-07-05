from Image_Class import Image_Class
import argparse
import os
from scipy.misc import imsave

parser = argparse.ArgumentParser()
parser.add_argument('--easy_folder', type = str)
parser.add_argument('--hard_folder', type = str)
parser.add_argument('--output_folder', type = str)
args = parser.parse_args()


def combined_image(image_path_easy, image_path_hard):
	easy_image = Image_Class(image_path_easy)
	hard_image = Image_Class(image_path_hard)

	return easy_image.combine(hard_image)


def get_images(easy_folder, hard_folder, output_folder):
	easy_image_paths = []
	for each in os.listdir(easy_folder):
		easy_image_paths.append(os.path.join(easy_folder, each))

	hard_image_paths = []
	for each in os.listdir(hard_folder):
		hard_image_paths.append(os.path.join(hard_folder, each))

	# Save combined images
	for i in range(len(easy_image_paths)):
		current_image = combined_image(easy_image_paths[i], hard_image_paths[i])
		output_path = os.path.join(output_folder, "combined_" + easy_image_paths[i].split('/')[-1] + hard_image_paths[i].split('/')[-1])
		imsave(output_path, current_image)



# MAIN #
if os.path.exists(args.output_folder):
	os.system('rm -r ' + args.output_folder)

os.system('mkdir ' + args.output_folder)

get_images(args.easy_folder, args.hard_folder, args.output_folder)
