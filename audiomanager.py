import os
#import sys
import shutil
import librosa
import moviepy.editor as mp
import soundfile
import pydub
import wave
import contextlib
import pysrt
from gtts import gTTS

from pydub import AudioSegment
from pydub import effects



## to convert input video to wav with sr =16k
def convert2wav(inputFile):
	global clip 

	clip = mp.VideoFileClip(inputFile)

	clip.audio.write_audiofile("arnold.wav")

	y,s = librosa.load('arnold.wav',sr =16000)

	soundfile.write('converted.wav',y, samplerate=16000)
	os.remove("arnold.wav")
	with open("file.txt","w") as f:
		f.write(inputFile)


## to make a silent long 
def makesilent():
	fname = 'converted.wav'
	duration = 0
	with contextlib.closing(wave.open(fname,'r')) as f:
	    frames = f.getnframes()
	    rate = f.getframerate()
	    duration = frames / float(rate)

	second_of_silence = AudioSegment.silent(duration=duration*1000)
	second_of_silence.export(out_f = "silent.wav", format = "wav")    

##save chunks of translated audio into a folder
def makechunks():
#	print(newlang)
	with open('texts_generated/lang.txt','r') as f:
		newlang = f.read()
	makesilent()
	global duration
	global startpositon
	startpositon = []
	duration = []
	subs = pysrt.open('texts_generated/translated_sub.srt')
	i = 0
	for sub in subs:
		sen = sub.text
		k = float(sub.duration.seconds) + (sub.duration.milliseconds)/1000
		duration.append(k)
		y = ((sub.start.hours * 60 + sub.start.minutes) * 60 + sub.start.seconds) * 1000 + sub.start.milliseconds
		startpositon.append(y)
		audio = gTTS(text = sen, lang = newlang, slow = False)
		audio.save('uploads/chunks/{}.wav'.format(i))
		i+=1
				



def speedupAudio():
	try:
		os.mkdir('uploads/chunks/audio2')
	except:
		pass

	veloctiy = []	
	for i in range(len(duration)):
		aud = mp.AudioFileClip('uploads/chunks/{}.wav'.format(i))
		real_length = aud.duration
		new_time = round(real_length/duration[i] , 3)
		veloctiy.append(new_time)
	print(AudioSegment.ffmpeg)	
	AudioSegment.converter = r"ffmpeg/ffmpeg.exe"
	AudioSegment.ffprobe = r"ffmpeg/ffprobe.exe"

	for i in range(len(duration)):
		root = r'uploads/chunks/{}.wav'.format(i)
		
		sound = AudioSegment.from_file(root)
		so = sound.speedup(new_time,50,100)
		so.export('uploads/chunks/audio2/{}new.wav'.format(i),format= 'wav')

	

def makeAud():
	silent = AudioSegment.from_file('silent.wav')
	for i in range(len(duration)):
		root = r'uploads/chunks/audio2/{}new.wav'.format(i)
		sound_file = AudioSegment.from_file(root)
		silent = silent.overlay(sound_file,position = startpositon[i])



	
	silent.export('translated_aud.wav', format = "wav")

def makeVid():
	#makechunks(language)
	try :
		videoF = clip.set_audio(mp.AudioFileClip('translated_aud.wav'))
	except:
		with open("file.txt",'r') as f:
			ip = f.read()

		clip = mp.VideoFileClip(ip)
		videoF = clip.set_audio(mp.AudioFileClip('translated_aud.wav'))	
	
	videoF.write_videofile('new_video.mp4')
	removeUnwanted()

def removeUnwanted():
	try :
		os.remove('silent.wav')
		# os.remove('texts_generated/temp.srt')
		os.remove('texts_generated/temp2.srt')
		#os.remove('texts_generated/file.srt')
		os.remove('texts_generated/temp3.srt')
		
		#os.remove('texts_generated/update.txt')
		os.remove('texts_generated/text.txt')
		os.remove('a.wav')
		os.remove('converted.wav')
		shutil.rmtree('uploads/chunks')
	except:
		pass	



########################################################################
########################## Functions for sensoring #####################
########################################################################

def readWords():
	

	with open("model/predefined.txt","r") as f1:
		words_ = set (f1.read().split())


	with open("texts_generated/words_to_filter.txt") as f2:
		user_words_ = set(f2.read().split())	
  

	ret = words_.union(user_words_)	
	return ret




def sensorFn():

	list_1 = readWords()

	print(list_1)
	st_po = []
	en_po = []

	file = pysrt.open("texts_generated/file.srt")
	
	for sub in file:
		wrd = sub.text
		

		if wrd in list_1:
			
			y = ((sub.start.hours * 60 + sub.start.minutes) * 60 + sub.start.seconds) * 1000 + sub.start.milliseconds 
			j = ((sub.end.hours * 60 + sub.end.minutes) * 60 + sub.end.seconds) * 1000 + sub.end.milliseconds 
			st_po.append(y)
			
			en_po.append(j)
			

	

	# for i in range(len(st_po)):
		
	# 	dur = en_po[i] - st_po[i]
	# 	#silent_aud = AudioSegment.silent(duration=dur) 
	# 	# print("made silent", dur)
	# 	# silent_aud.export("texts_generated/{}.wav".format(i), format = "wav")
	# 	beep = AudioSegment.from_file('model/beep.wav')
	# 	beep = beep[st_po[i]:en_po[i]]
	# 	beep.export("texts_generated/{}.wav".format(i), format = "wav")

	og_file = AudioSegment.from_file('converted.wav')

	for i in range(len(st_po)):
		#root = r'texts_generated/{}.wav'.format(i)
		sound_file = AudioSegment.from_file('model/beep.wav')
		sound_file = sound_file + 10
		print(st_po[i])
		og_file = og_file.overlay(sound_file,position = st_po[i])
	
	og_file.export('sensored_aud.wav', format = 'wav')
	
	try :
		videoF = clip.set_audio(mp.AudioFileClip('sensored_aud.wav'))
	except:
		with open("file.txt",'r') as f:
			ip = f.read()

		clip = mp.VideoFileClip(ip)
		videoF = clip.set_audio(mp.AudioFileClip('sensored_aud.wav'))		

	videoF.write_videofile('new_video.mp4')	