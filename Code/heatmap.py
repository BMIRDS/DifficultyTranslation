import cv2
import numpy as np 
from scipy.misc import imsave

#INPUT_ should be [true_negatives, false_negatives]

# TUBULAR
#Louis Vaickus (p1)
# input_ = [88, 81]

#Bing Ren (p2)
# input_ = [90, 83]

#Xiaoying Liu (p3)
# input_ = [97, 94]

#Arief Suriawinata (p4)
# input_ = [87, 62]

#Average
# input_ = [90.5, 80]



# SESSILE SERRATED
#Louis Vaickus (p1)
# input_ = [80, 23]

#Bing Ren (p2)
# input_ = [100, 74]

#Xiaoying Liu (p3)
# input_ = [99, 91]

#Arief Suriawinata (p4)
# input_ = [99, 97]

#Average
input_ = [94.5, 71.25]

image = np.zeros((81, 1006, 3))


image[3:78, 3:(int)(input_[0]*1.0/100*450+3), :] = [0, 255, 0]
image[3:78, (int)(input_[0]*1.0/100*450+3):454, :] = [255, 0, 0]

image[3:78, 553:(int)(input_[1]*1.0/100*450+554), :] = [0, 255, 0]
image[3:78, (int)(input_[1]*1.0/100*450+554):1003, :] = [255, 0, 0]

image[:, 458:550, :] = [255, 255, 255]

imsave('output.png', image)










