import os
import datetime
from subprocess import call

def is_valid_file(filename):
	try:
		if(filename.index('-')):
			return True
	except Exception:
		return False

def get_creation_date(filename):
	d = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
	return "{0}_{1}_{2}_{3}_{4}_{5}".format(d.day, d.month, d.year, d.hour, d.minute, d.second)


def strip_filename(filename):
	return filename.split('-')[0]

def gen_filename(filename):
	return "{0}_{1}".format(strip_filename(filename), get_creation_date(filename))


def gen_video(inputFilename, outputFilename):
	print("Encoding {0} to {1}".format(inputFilename, outputFilename))
	# call(["ffmpeg", "-i", inputFilename, "-c:v", "libx264", "-b:v", "250k", "-bufsize", "125k", "-vf", "scale=iw*0.75:ih*0.75", "-r", str(15), "-c:a", "libvo_aacenc", "-b:a", "64k", "-ac", str(1), "output/{0}.mp4".format(outputFilename)])
	# call(["ffmpeg", "-i", inputFilename, "-c:v", "libx264", "-crf", "23", "-c:a", "aac", "output/{0}.mp4".format(outputFilename)])
	# call(["ffmpeg", "-i", inputFilename, "-c:v", "libx264", "-vf", "scale=iw*0.75:ih*0.75", "-c:a", "aac", "output/{0}.mp4".format(outputFilename)])
	call(["ffmpeg", "-i", inputFilename, "-c:v", "libx264", "-r", "30", "-c:a", "aac", "-max_muxing_queue_size", "9999", "output/{0}.mp4".format(outputFilename)])


for f in os.listdir(os.curdir):
	if(is_valid_file(f)):
		gen_video(f, gen_filename(f))
		#print(gen_filename(f))