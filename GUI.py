#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*

# modules
from tkinter import *
import cv2 as cv
import numpy as np
from math import *
from PIL import (Image, ImageTk)
import tkinter.filedialog


class Interface(Frame):
	"""Homemade class that contains our graphical interface.
	This class inherits from Frame.
	
	Attributes:
	- 

	Methods:
	-


	"""

	def __init__(self, window, **kwargs):
		"""Class initiator."""
		
		# Interface initialization
		Frame.__init__(self, window, width=1000, height=800, **kwargs)
		self.pack()

		# Attributes
		self.image = None
		self.src_width = 0
		self.src_height = 0
		self.pattern = None
		self.ptn_width = 0
		self.ptn_height = 0
		self.outcome = None
		self.out_width = 0
		self.out_height = 0
		self.F = 0
		self.img = None

		# Widgets

		# First the canvas on which we will print the pattern
		self.canvas = Canvas(self, bg='white', height=500, width=500)
		self.canvas.pack(side=LEFT)


		# Then buttons!
		self.quit_button = Button(self, text="Quit", width=15, command=self.quit)
		self.quit_button.pack(side=BOTTOM)
		self.load_button = Button(self, text="Load image", width=15, command=self.STSload)
		self.load_button.pack()
		self.convert_button = Button(self, text="Convert !", width=15, command=self.STSpixelate)
		self.save_button = Button(self, text="Save pattern", width=15, command=self.STSsave)

		# Conversion widgets
		self.img_label1 = Label(self, text="")
		self.img_label2 = Label(self, text="")
		self.size_label = Label(self, text="Please type the max. number of stitches in the largest dimension:")
		self.size_field = Entry(self, bg='white')
		self.ptn_label1 = Label(self, text="")
		self.ptn_label2 = Label(self, text="")
		self.ptn_label3 = Label(self, text="")

	def STSload(self):
		"""This method imports an image, and writes the corresponding pixel array into attribute image."""

		#Read the path from the entry -> should be included in a try/except bloc!!!
		src_path = tkinter.filedialog.askopenfilename()

		#Load the image -> should be included in a try/except bloc!!!
		self.image = cv.imread(src_path)
	
		#Check! -> should be included in a try/except bloc!!!
		while self.image is None:
			self.import_label["text"] = "Invalid path. Please try again!"
			src_path = str(self.import_field.get())
			self.image = cv.imread(src_path)


		#Retrieve the source image parameters
		self.src_width = self.image.shape[1]
		self.src_height = self.image.shape[0]
		
		self.img_label1["text"] = "Image width: {}".format(self.src_width)
		self.img_label1.pack()
		self.img_label2["text"] = "Image height: {}".format(self.src_height)
		self.img_label2.pack()

		#Show the image in the canvas
		self.canvas.delete(ALL)
		self.canvas.config(width=self.src_width, height=self.src_height)				#adjusting canvas to image size
		self.img = cv.cvtColor(self.image, cv.COLOR_BGR2RGB)							#convert it to RGB
		self.img = Image.fromarray(self.img, 'RGB')										#convert it to PIL format
		self.img = ImageTk.PhotoImage(image=self.img)									#convert it to Tkinter format
		self.canvas.create_image(self.src_width/2, self.src_height/2, image=self.img)	#and finally show it into the canvas

		#Ask user about the size of the pattern
		self.size_label.pack()
		self.size_field.pack()
		self.size_field.bind("<Return>", self.STSsize)
		
	def STSsize(self, event):
		"""This method makes the user choose the max. largest dimension of the pattern."""

		src_max = max(self.src_width, self.src_height)
		user_max = self.size_field.get()

		#Check and convert into an integer
		try:
			user_max = int(user_max)
		except ValueError:
			self.size_label["text"] = "Invalid size: should be an integer between 1 and {}.\n".format(src_max)
			user_max = self.size_field.get()
		else:
			if user_max >= src_max:
				self.size_label["text"] = "Invalid size: should be an integer between 1 and {}.\n".format(src_max)
				user_max = self.size_field.get()

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
		if self.src_width >= self.src_height:
			self.ptn_width = ptn_max
			self.ptn_height = ceil(self.ptn_width * self.src_height / self.src_width)
			self.F = round(self.src_width / self.ptn_width)
		else:
			self.ptn_height = ptn_max
			self.ptn_width = ceil(self.ptn_height * self.src_width / self.src_height)
			self.F = round(self.src_height / self.ptn_height)
	
		#Show theses parameters to the user and invite them to convert
		self.ptn_label1["text"] = "Pattern width: {} stitches".format(self.ptn_width)
		self.ptn_label1.pack()
		self.ptn_label2["text"] = "Pattern height: {} stitches".format(self.ptn_height)
		self.ptn_label2.pack()
		self.ptn_label3["text"] = "Resizing factor: {}".format(self.F)
		self.ptn_label3.pack()

		self.convert_button.pack()


	def STSpixelate(self):
		"""This function converts an image into a Xstitch pattern.
		It is pixelated to the largest dimension chosen by user by applying an arithmetic average of colors from adjacent pixels."""

		#Create the pattern
		self.pattern = np.zeros((self.ptn_height, self.ptn_width, 3), dtype = self.image.dtype)

		#Pixelate!!!

		for i in range(0, self.ptn_height):
			for j in range(0, self.ptn_width):
				extract = np.array(self.image[i*self.F:(i+1)*self.F, j*self.F:(j+1)*self.F])
				blue = np.mean(extract[:,:,0])
				green = np.mean(extract[:,:,1])
				red = np.mean(extract[:,:,2])
				self.pattern[i,j] = [blue, green, red]

			#Something I don't get here... There should be a problem with bigger indexes (i,j) when they reach the boundaries of the source image in the previous loop...
			#All my tests work so far, I imagine NumPy has a "truncature" function that enables to create extract array even if the indexes are too great...
			#I will have to test further images, and investigate that loop, to ensure there is no nasty hidden bug!

		#Show the pattern in the canvas
		
		self.STSshowpattern()

		#Propose to save the pattern
		self.save_button.pack()

	def STSshowpattern(self):


		#Show the outcome in the canvas
		#The idea is to make the pattern more readable by increasing the size of each pixel and adding a grid
		
		#Create the outcome image
		self.out_width = self.F * self.ptn_width
		self.out_height = self.F * self.ptn_height
		self.outcome = np.zeros((self.out_height, self.out_width, 3), dtype = self.image.dtype)

		for i in range(0, self.ptn_height):
			for j in range(0, self.ptn_width):
				for a in range(i*self.F,(i+1)*self.F):
					for b in range(j*self.F,(j+1)*self.F):
						self.outcome[a,b] = self.pattern[i,j]
		

		#Refresh the canvas
		self.canvas.delete(ALL)
		self.canvas.config(width=self.out_width, height=self.out_height)					#adjusting canvas to outcome size
		
		#Display the outcome
		self.img = cv.cvtColor(self.outcome, cv.COLOR_BGR2RGB)								#convert it to RGB
		self.img = Image.fromarray(self.img, 'RGB')											#convert it to PIL format
		self.img = ImageTk.PhotoImage(image=self.img)										#convert it to Tkinter format
		self.canvas.create_image(self.out_width/2, self.out_height/2, image=self.img)		#and finally show it into the canvas

		#Display the grid



	def STSsave(self):
		"""This method saves the pattern to a file on user's computer."""

		#Possible file types
		STS_files = [
			('All files', '*,*'),
			('JPEG image', '*.jpg'),
			('PNG image', '*.png'),
			]

		#Make the user choose a path -> should be included in a try/except bloc!!!
		ptn_path = tkinter.filedialog.asksaveasfilename(filetypes=STS_files, defaultextension='.png')

		#Save the pattern into that file
		cv.imwrite(ptn_path, self.outcome)


	

