import serial

import time

import sys

import requests



class serial_SensorTile():



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

				data = line.split('\t')

				# str to float and store dis, accel

				try:

					print ("{}".format(data))
					print ("sending data")


					#url = "https://api.myjson.com/bins/1duknl"
					url = "https://api.myjson.com/bins/jub2l"

		
					headers = {'Content-type': 'application/json'}


					#datas = {"color":"pink","speed":data[1],"pulse":1, "number":17}
					datas = {"360Rotation":888,"slideBrightness":0.5,"slideNumber":data[1],"animationIsPlaying":0,"dismissPresentation":0}
					rsp = requests.put(url, json=datas, headers=headers)


					dis = float(data[0])

					accel = float(data[1])

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



