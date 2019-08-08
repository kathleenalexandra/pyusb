import serial

import time

import sys

import requests

class serial_SensorTile():

	Xvalue = 0;
	Yvalue = 0;
	Zvalue = 0; 
	slideNum = 0; 
	slideOrientation = 0
	url = "https://api.myjson.com/bins/jub2l"
	headers = {'Content-type': 'application/json'}
						#datas = {"color":"pink","speed":data[1],"pulse":1, "number":17}
	


	def __init__(self, address, baud_rate=9600, timeout=2, python3=False):

		self.ser = None

		self.last_line = ""

		# serial information

		self.address = address

		self.baud_rate = baud_rate

		self.timeout = timeout

		# flag 

		self.data_check = 0

		self.python3 = python3


	def init_connection(self):

		print ("Start Serial Connection")

		try:

			ser = serial.Serial(self.address, self.baud_rate, timeout=self.timeout)

		except:

			print ("Wrong serial address and shut donw system")

			sys.exit()

		self.ser = ser

		# sleep 500ms before accepting data

		time.sleep(0.5)

		self.ser.flushInput()



	def close_connection(self):

		print ("Close Serial Connection")

		self.ser.close()

		

	def is_ready(self, bytes_expected):

		return self.ser.in_waiting >= bytes_expected



	def collect_data(self):

		if self.data_check:

			# read all new bytes

			bytesToRead = self.ser.in_waiting

			ser_bytes = self.ser.read(bytesToRead)

			# convert byte to string python 3

			if self.python3:

				ser_bytes = ser_bytes.decode("utf-8")

			ser_bytes = self.last_line + ser_bytes  # prepend previous unfinished line

			ser_bytes = ser_bytes.split('\n')       # split lines

			self.last_line = ser_bytes[-1]          # save unfinished line

			ser_bytes = ser_bytes[0:-1]             # discard unfinished line

			dis_list = []

			accel_list = []

			

			for line in ser_bytes:

				# discard \r

				line = line.rstrip()


				# split data

				data = line.split(',')

		


				# str to float and store dis, accel

				try:
					#print "newtest"
				
					#print ("{}".format(data))
					
				
					print "x"
					print data[0]
					print "y" #Z
					print data[1]
					print "z"
					print data[2]
			
					###print data[3] #GX
					##print data[2] #GY
					##print data[4] #GZ

				
					dis = float(data[0])
					accel = float(data[1])



					if int(data[0]) < -800:
						print "turn left"
						self.slideNum-=1
						print self.slideNum
						datas = {"360Rotation":0,"slideBrightness":24,"slideNumber":self.slideNum,"animationIsPlaying":0,"dismissPresentation":0}
						rsp = requests.put(self.url, json=datas, headers=self.headers)


				
					elif int(data[0]) > 800:
						print "turn right"
						self.slideNum+=1
						print self.slideNum


					elif int(data[1]) > 100:
						if int(self.Yvalue) < -100:
							print "moved forward"
							#self.slideOrientaton+=60
							#if self.slideOrientaton >= 360:
								#self.slideOrientation = 0
						else:
							print "" 
					else:
						print ""


					
					"""if int(data[1]) < -1000:
						if self.Yvalue > -10:
							#stime.sleep(5) 
							print "#########################"
							self.slideNum+=1
							print self.slideNum
						else:
							print "" """



					self.Xvalue = data[0]
					self.Yvalue = data[1]
					self.Zvalue = data[2]

					#print Xvalue
					#print Yvalue
					#print Zvalue


					# print ("{}".format(dis))

					# print ("{}".format(accel))

					dis_list.append(dis)

					accel_list.append(accel)

				except:

					print ("Wrong serial read:")

					dis_list.append(0)

					accel_list.append(0)

			return dis_list, accel_list

		else:

			# discard the first corrupted line

			self.ser.reset_input_buffer()

			self.ser.readline()

			self.data_check = 1

			return [], []



