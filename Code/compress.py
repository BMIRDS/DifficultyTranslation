import cv2 
from scipy.misc import imsave
import argparse
import os
from Image_Class import Image_Class

parser = argparse.ArgumentParser()
parser.add_argument("--input_folder", type = str, help = "input path to folder containing images to be modified")
parser.add_argument("--output_folder", type = str, help = "folder name for resulting images")
parser.add_argument("--compress", type = str, default = 'False', help = "True or False - true = images will be compressed")
parser.add_argument("--filter_dups", type = bool, default = True, help = "True or False - true = duplicates will be removed")
parser.add_argument("--add_AtoB", type = str, default = 'False', help = "True or False - true = AtoB_ will be added in front")
parser.add_argument("--compression_factor", type = float, default=1.0, help = "e.g. convert 256 --> 224 should input (256/224), if not compressing put any number")
parser.add_argument("--increase_brightness", type = str, default = 'False', help = 'True or False - true = increase the brightness of the pictures')
args = parser.parse_args()

add_AtoB = False
if args.add_AtoB == "true" or args.add_AtoB == "True":
	add_AtoB = True

compress = False
if args.compress == 'true' or args.compress == "True":
	compress = True

brightness = False
if args.increase_brightness == 'True' or args.increase_brightness == 'true':
	brightness = True

if not os.path.exists(args.output_folder):
	os.makedirs(args.output_folder)


for each in os.listdir(args.input_folder):

	if args.filter_dups == True and "dup" in each:
		continue

	if each == ".DS_STORE" or '.html' in each:
		continue

	filepath = os.path.join(args.input_folder, each)

	current_image = Image_Class(filepath)

	if compress == True:
		current_image.compress(args.compression_factor)

	if brightness == True:
		current_image.increase_brightness(75)

	if add_AtoB == True:
		# output_path = os.path.join(args.output_folder, "AtoB_" + each.split[:-4] + ".png")
		output_path = os.path.join(args.output_folder, "AtoB_" + each[:-4] + ".png") #For real images
		imsave(output_path, current_image.get_image())
	else:
		output_path = os.path.join(args.output_folder, each[:-4] + ".png") #For fake images
		# output_path = os.path.join(args.output_folder, each.split(".")[1][2:] + ".jpg") #For real images
		current_image.save_image(output_path)










