import cv2 as cv
import numpy as np
import re
import os
import sys
from PIL import Image
#checks for argument(dir or file), calls functions.
def main():
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            directory = sys.argv[1]
            separate_images(os.listdir(directory),directory)
        elif os.path.isfile(sys.argv[1]) and re.search(r'^.+\.(jpg|png)$', (sys.argv[1])):
            image_file = []
            image_file.append(get_path(sys.argv[1]))
            resize(image_file)
        else:
            print("invalid path argument")
        
    else:
        directory = (os.getcwd())
        separate_images(os.listdir(directory),directory)
        print(directory + "\\")

#search through the folder for the path to all jpg or png filles in the folder and store these vallues in image_files list
def separate_images(files,directory):
    image_files = []
    for file in files:
        if re.search(r'^.+\.(jpg|png)$', file):
            image_files.append(directory + '\\' + file)
    resize(image_files)
    
#converts into rgba, changes into transparent pixels for png, saves in png
def convertImage(image_files_a):
    for image_file in image_files_a:
        img = Image.open(image_file)
        img = img.convert("RGBA")
    
        datas = img.getdata()
    
        newData = []
    
        for item in datas:
            if (item[0] == 255 and item[1] == 255 and item[2] == 255) or (item[0] == 0 and item[1] == 0 and item[2] == 0):
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
    
        img.putdata(newData)
        img.save((image_file.rstrip(image_file[-3:]))+ 'png')
        print("Successful")
#resizes with opencv
def resize(image_files):
    image_files_a = []
    for image_file in image_files:
        image = cv.imread(image_file)
        a, b, c = (image.shape)
        if a == b and a < 150:
            pass
        elif a == 288 or b == 288 or a == 144:
            pass
        elif (b / a) < 1.2 and b/a > 0.8:
            res = cv.resize(image, dsize=(144,144))
            cv.imwrite(((image_file.rstrip(image_file[-3:]))+ 'png'), res)
            image_files_a.append((image_file.rstrip(image_file[-3:]))+ 'png')
        else:
            res = cv.resize(image, dsize=(576,288))
            cv.imwrite(((image_file.rstrip(image_file[-3:]))+ 'png'), res)
            image_files_a.append((image_file.rstrip(image_file[-3:]))+ 'png')
        
        print(image_file , "done")
    convertImage(image_files_a)
#path for when input is a file, to get directory.
def get_path(file):
    file = re.split(r"\\", file)
    new_path = "C:"
    for fil in file[1:-1]:
        new_path = new_path +"\\" + fil
    
    return str(new_path)
