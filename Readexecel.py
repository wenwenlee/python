import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
 
df = pd.read_excel('D:\\code\\NotePad\\SCUT-FBP5500_v2\\All_Ratings2.xlsx', sheet_name='Asian_Female')

data = df["Rating"]
print(data[3])
sum = 0
for i in range(60) :
	sum = sum + data[i]
adverage = sum/60	
result = ("%.2f" % adverage)#保留指定位数的小数
print(adverage)
print(result)
