# -*- coding:utf-8 -*-

"@author: LWT"

import os

for file in os.listdir('.'):
	if file[-2: ] == '3d':
		
		new_name = file[1:7] + '.txt'
		os.rename(file,new_name)	
	
