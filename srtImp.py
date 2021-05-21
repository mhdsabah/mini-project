from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import subprocess
import srt
import json
import datetime
import pysrt

sample_rate=16000
model = Model("model")
rec = KaldiRecognizer(model, sample_rate)

# process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
#                             sys.argv[1],
#                             '-ar', str(sample_rate) , '-ac', '1', '-f', 's16le', '-'],
#                             stdout=subprocess.PIPE)





def transcribe(input_file,wp):
  WORDS_PER_LINE = wp
  #process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',input_file,'-ar', str(sample_rate) , '-ac', '1', '-f', 's16le', '-'],stdout=subprocess.PIPE)
  results = []
  subs = []

  input_file.read(44)
  while True:
       data = input_file.read(4000)
       if len(data) == 0:
           break
       if rec.AcceptWaveform(data):
           results.append(rec.Result())
  results.append(rec.FinalResult())

  for i, res in enumerate(results):
       jres = json.loads(res)
       if not 'result' in jres:
           continue
       words = jres['result']
       for j in range(0, len(words), WORDS_PER_LINE):
           line = words[j : j + WORDS_PER_LINE] 
           s = srt.Subtitle(index=len(subs), 
                   content=" ".join([l['word'] for l in line]),
                   start=datetime.timedelta(seconds=line[0]['start']), 
                   end=datetime.timedelta(seconds=line[-1]['end']))
           subs.append(s)
  return subs



def createText():
  srtfile = pysrt.open("texts_generated/file.srt")
  txtfile = open("texts_generated/text.txt","w")
  strtn = ""

  for sub in srtfile:
    tx = sub.text

    txtfile.write(tx+" ")
    strtn+=tx+"\n"
   
  #srtfile.close()
  txtfile.close()  
  return strtn