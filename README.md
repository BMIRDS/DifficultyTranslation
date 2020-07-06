# Difficulty Translation

Code for the paper "[Difficulty Translation in Histopathology Images](https://arxiv.org/pdf/2004.12535.pdf)".

[Jerry Wei](https://github.com/JerryWei03), Arief Suriawinata, Xiaoying Liu, Bing Ren, Mustafa Nasir-Moin, Naofumi Tomita, Jason Wei, and Saeed Hassanpour.

## Packages used (dependencies):
- Numpy 1.15.2
- PyTorch 0.4.1
- Torchvision 0.2.1
- SciPy 1.3.0
- Seaborn 0.9.0
- Matplotlib 3.0.0
- Pandas 0.23.4
- OpenCV 3.4.2
- Scikit-Image 0.14.0
- Scikit-Learn 0.20.0
- Pillow 6.0.0
- Tensorflow-GPU 1.4.0

## Folders included in this repository:
1. Code - all code used to analyze images (e.g. selecting images based on confidence)
2. CycleGAN - all code used to train CycleGAN models. Original implementation from [xhujoy](https://github.com/xhujoy/CycleGAN-tensorflow).
3. ResNet - all code used to train ResNet classifier models. Original implementation from [BMIRDS](https://github.com/BMIRDS/deepslide).

## Basic Usage
### 1. Train Generative Model
A. Training CycleGAN
  - Make a `datasets/class1TOclass2/` folder
      - Subfolders: trainA (training images for class #1), trainB (training images for class #2), testA (original class 
        #1 images that will be used to generate fake class #2 images), testB (original class #2 images that will be used to 
        generate fake class #1 images)
  - Run `CycleGAN/main.py` and specify options with argparse (look at main.py for details about parameters); --phase should be 
    "train"
  - To run difficulty translation as in our paper, ensure that trainA consists of "easy" images and trainB consists of "hard" images. Images can be determined as "easy" or "hard" with your own threshold depending on your dataset.
  
### 2. Generating Synthetic Images
A. Using CycleGAN
  - Run `CycleGAN/main.py` and specify options with argparse; --phase should be "test"
  - Generated images can be viewed in `CycleGAN/test/*.jpg`

### 3. Training new ResNet with generated images
A. Data preparation
  - ResNet training requires `train_folder/train/class1/`, `train_folder/train/class2/`, `train_folder/val/class1`, 
    `train_folder/val/class2`
  - Move generated images and real images into respective training and validation folders
B. Train ResNet
  - Run `ResNet/3_train.py` and specify options (e.g. number of layers) in `ResNet/config.py`
  - Models will be saved in `ResNet/checkpoints/`
