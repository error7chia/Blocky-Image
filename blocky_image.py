#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 16:03:24 2024

@author: alfie
"""

import numpy as np
from PIL import Image
import math
import os

def image_to_pixel_blocks(path, block_size, subblock_size, output):
    # convert picture
    image = Image.open(path).convert("L")
    
    width, height = image.size
    
    # convert into numpy array
    pixel_data = np.array(image)

    # create the block image
    new_height = height - height % block_size
    new_width = width - width % block_size
    #print(new_height,new_width)  #debug
    block_image = np.ones((new_height, new_width), dtype=np.uint8) * 255  # initialise as white
    
    # pixel_data[i,j] is the gray value of the pixel
    pixel_per_block = block_size ** 2
    block_subblock_number = pixel_per_block / (subblock_size **2)
    
    
    # going through every block and decide whether a block should be black or white
    for i in range(0, new_height, block_size):
        for j in range(0, new_width, block_size):
            #now we are at the very corner of the block
            total_grey_value = 0
            for k in range(block_size):
                for l in range(block_size):
                    total_grey_value += pixel_data[i+k, j+l]
            subblock = round((1 - (total_grey_value / pixel_per_block /225)) * block_subblock_number) #black subblock number of the block
            #print(subblock)  #debug
            if subblock >=0:
                depth = round(math.sqrt(subblock) * subblock_size)
            else:
                depth = 0
            for k in range(i, i + depth, 1):
                for l in range(j, j + depth, 1):
                    block_image[k, l] = 0
            
    os.chdir(output)
    block_image = Image.fromarray(block_image)
    block_image.save(fp = "blocky_image.png")

# sample use
a = input("Input path of the image: ")
b = int(input("Input block size: "))
c = int(input("input subblock size (block size must be divisible by it): "))
d = input("Output directory: ")
image_to_pixel_blocks(a,b,c,d)