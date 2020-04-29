#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*

#modules
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from math import *

def STSimport():
	"""This function imports an image, ideally chosen by the user, and returns the corresponding pixel array."""

	#Make the user choose an image to convert
	print("Please type the path to an image to convert into a Xstitch pattern:")
	src_path = str(input())

	#Load the image
	image = cv.imread(src_path)

	#there I should raise exceptions :)

	return image

def STSconvert(source):
	"""This function converts an image into a Xstitch pattern.
	User is prompted to choose the max. largest dimension of the pattern, then image is pixelated to that largest dimension by applying an arithmetic average of colors from adjacent pixels."""

	#Retrieve the source image parameters	
	src_width = source.shape[1]
	src_height = source.shape[0]
	print("Image width: {}\nImage height: {}".format(src_width, src_height))	#double checked to avoid mismatching width and height
	src_max = max(src_width, src_height)

	#Ask user about the size of the pattern
	print("Please type the desired size of the pattern (in number of stitches in the largest dimension):")
	user_max = int(input())

	#there I should raise exceptions :)

	#Find the dimensions of the pattern
	
	#First we find the nearest integer that divides the largest dimension of the source image -> this integer is gonna be our pattern largest dimension (ptn_max)
	diff = src_max
	ptn_max = 0
	for n in range(1, src_max):
		if src_max % n == 0:
			if abs(user_max - n) < diff:
				ptn_max = n
				diff = abs(user_max - n)

	#Now we calculate the dimensions of the pattern
	if src_width >= src_height:
		ptn_width = ptn_max
		ptn_height = ceil(ptn_width * src_height / src_width)
		F = round(src_width / ptn_width)
	else:
		ptn_height = ptn_max
		ptn_width = ceil(ptn_height * src_width / src_height)
		F = round(src_height / ptn_height)
	
	print("Pattern width: {} stitches\nPattern height: {} stitches".format(ptn_width, ptn_height))
	print("Resizing factor: {}".format(F))

	#Create the pattern
	pattern = np.zeros((ptn_height, ptn_width, 3), dtype = int)

	#Pixelate!!!

	for i in range(0, ptn_height):
		for j in range(0, ptn_width):
			extract = np.array(source[i*F:(i+1)*F, j*F:(j+1)*F])
			blue = np.mean(extract[:,:,0])
			green = np.mean(extract[:,:,1])
			red = np.mean(extract[:,:,2])
			pattern[i,j] = [blue, green, red]

			#Something I don't get here... There should be a problem with bigger indexes (i,j) when they reach the boundaries of the source image in the previous loop...
			#All my tests work so far, I imagine NumPy has a "truncature" function that enables to create extract array even if the indexes are too great...
			#I will have to test further images, and investigate that loop, to ensure there is no nasty hidden bug!

	return pattern





