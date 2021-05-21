from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import subprocess
import srt
import json
import datetime




def sttTest(input_file):#,outfile_text,outfile_srt):
	model = Model("model")

	rec = KaldiRecognizer(model , 16000)

	op = open("output.txt","w")

	input_file.read(44)

	while True:
		data = input_file.read(4000)
		if len(data) == 0:
			break
		if rec.AcceptWaveform(data):
			res = json.loads(rec.Result())
			#print(res['text'])	

			out_data = res['text']
			
			op.write(out_data)
			op.write(" ")
			

	res = json.loads(rec.FinalResult())
	
	#outfile_text.write(out_data)	
	