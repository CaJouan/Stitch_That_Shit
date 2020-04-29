#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*

#modules
from images import *
import matplotlib.pyplot as plt

#image load
src_img = STSimport()

#conversion into a Xstitch pattern
pattern = STSconvert(src_img)


plt.imshow(pattern[..., ::-1])	#affichage
plt.show()