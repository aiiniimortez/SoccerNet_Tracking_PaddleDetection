import os
import time

for i in range(12*3600):
	if i%102 == 0:
		print(i)
	time.sleep(1)
