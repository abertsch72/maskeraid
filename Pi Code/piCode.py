import os
import serial
from PIL import Image, ImageOps
from MaskClassifierClient import isMaskOn, isMaskOnCorrect
import time
import face_detect
'''
This code was built to run on a linux machine and is NOT OS agnostic
'''
os.system("echo " + os.path.abspath(os.getcwd()))
ser = serial.Serial("/dev/ttyACM0",2000000,timeout=5)
ser.flush()
if not os.path.exists(face_detect.IMAGE_DIR):
	os.makedirs(face_detect.IMAGE_DIR)
print("wait for input")
while True:
	
	if ser.in_waiting > 0:
		line = ser.readline().decode('utf-8').rstrip()
		print("got input")
		ser.flush()
		if line == "45":
			ser.write(b"Taking photo")
			print("taking a photo")
			os.system(f"streamer -f jpeg -o {face_detect.IMAGE_DIR}image.jpeg -s 1920x1080")
			ser.write(b"Stay patient")
			print("calling cv script")
			face_detect.mainScript();
			allwearingMask = True
			allwearmaskRight = True
			print("going into loop")
			currDir = face_detect.BW_DIR
			for img in os.listdir(currDir):
				print("going into content loop!")
				filepath = "{x}".format(x=currDir) + img
				'''
				if isMaskOn(filepath) == False:
					allwearingMask = False
				'''
				print(filepath)
				with open(filepath,'rb') as ff:
					content = ff.read()
				ff.close()
				print("mask off function call!!!")
				if isMaskOn(content) == False:
					allwearingMask = False
				elif isMaskOnCorrect == False:
					allwearmaskRight = False
		
			print("out of loop")
			if allwearingMask:
				ser.write(b"Mask Detected")			
				time.sleep(3)
				if allwearmaskRight:
					ser.write(b"*You may come in!")
				else:
					ser.write(b"*Put it on right")
			else:
				ser.write(b"Put on a mask")
			#og_image = Image.open("image{num}.jpeg".format(num=counter))
			#gray_image = ImageOps.grayscale(og_image)
			#gray_image.save("image{num}.jpeg".format(num=counter))
			print("deleting old pics")
			'''
			for img in os.listdir(currDir):
				filepath = "{x}".format(x=currDir) + img
				os.remove(filepath)
			'''

		if line == "99":
			ser.write(b"closing program")
			break

