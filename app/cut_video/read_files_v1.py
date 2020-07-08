#!/usr/bin/python
#coding = utf-8
# by chenwei 20200707

import os
import subprocess
import cv2

file_folder = "/data_1/data/video_test/cut"

# 运行命令
def run_cmd(cmd):
	res = subprocess.Popen(cmd,
							shell=True,
							stdout=subprocess.PIPE,
							stderr=subprocess.PIPE,)
	return res

def divtime(seconds):
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	return("%d:%02d:%02d" % (h, m, s))

def check_download_dir(dir):
	if not os.path.exists(dir):
	  os.makedirs(dir)
	pass

def read_txt_file(file_path, video_file):
	# arr = []
	f2 = open(file_path,"r")
	lines = f2.readlines()
	time_list =[]
	for line in lines:
		c_line = line.strip()
		# print(c_line)
		# print(len(c_line))  # 5
		size = int(len(c_line.split(" ")))

		if size>0:
			time = c_line.split(" ")
			# print("time", time)

			if len(time) == 2:
				# cut_file(time, video_file)
				time_list.append(time)
			elif len(time) == 3: #多个空格
				time = [time[0],time[2]]
				time_list.append(time)
				# cut_file(time, video_file)
	return time_list

def wirte_video(time_list,file):
	cap = cv2.VideoCapture(file)
	count = 0
	fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
	out = cv2.VideoWriter("xx",fourcc, 25.0, (1280,720),True)
	out.release()
	index = 0
	while cap.isOpened():
		ret, frame = cap.read()
		count += 1
		if frame is None:
			break
		if count ==  int(time_list[index][0])*25:
			dir = file.split('.mp4')[0]
			check_download_dir(dir)
			output_filename = "{0}_{1}.mp4".format(time_list[index][0],time_list[index][1])
			output_filpath = "{0}/{1}".format(dir,output_filename)
			out = cv2.VideoWriter(output_filpath,fourcc, 25.0, (1280,720),True)
		if count > int(time_list[index][0])*25 and count < int(time_list[index][1])*25:
			out.write(frame)
		if count == int(time_list[index][1])*25:
			out.write(frame)
			out.release()
			index=+1


def cut_file(time, file_path):
	start_time = divtime(int(time[0]))
	end_time = divtime(int(time[1]))
	# duration = end_time - start_time
	dir = file_path.split('.mp4')[0]
	check_download_dir(dir)
	output_filename = "{0}_{1}.mp4".format(start_time,end_time)
	output_filpath = "{0}/{1}".format(dir,output_filename)
	fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
	out = cv2.VideoWriter(output_filpath,fourcc, 25.0, (1280,720),True)
	# command = "ffmpeg  -i  {0} -vcodec copy -acodec copy -ss  {1} -to  {2}   {3} -y".format(video_file, start_time, end_time, output_filpath)
	# command = "ffmpeg -ss {0} -t {1} -accurate_seek -i {2} -codec copy  {3}".format(start_time,duration, video_file, output_filpath)
	print(command)
	# run_cmd(command)



file_list = os.listdir(file_folder)
for file in file_list:
	if file.endswith('.txt'):
		file_path = os.path.join(file_folder,file)
		video_file =   file_path.split('.txt')[0] + ".mp4"
		print(file_path)
		print(video_file)
		time_arrs = read_txt_file(file_path, video_file)
		wirte_video(time_arrs,video_file)
		# print(time_arrs)