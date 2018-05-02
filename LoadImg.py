import os
from numpy import *
import matplotlib.pyplot as plt
from PIL import Image


def load_data(FilePath):

	#读入文件列表，FilePath代表文件路径    
	filelist = [os.path.join(FilePath, f) for f in os.listdir(FilePath)]    
	
	x_train = []   
	y_train = []    
	n1 = len(filelist)    
	
	for img in filelist:   
		#将图像格式转为numpy数组格式  
		im = array(Image.open(img))
		x_train.append(im)   

	
	
	#print(x_train[2])
if __name__ == "__main__":    

	filePath = "D:\\code\\NotePad\\val_dir\\Cap"
	load_data(filePath)
