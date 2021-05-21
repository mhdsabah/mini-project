from flask import Flask, redirect, url_for, render_template, request,send_from_directory,flash,send_file

app = Flask(__name__)
import os
import srt

import srtImp
import pysrt
import audiomanager

import text2srt

import demo_play_with_model
#import moviepy.editor as mp


import voskFunction

UPLOAD_FOLDER = 'uploads'



app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER






@app.route("/" , methods = ["GET","POST"])
def upload_file():
	if request.method == "POST":

		
		if request.form.get('todo') == "sg&mt":

			f = request.files['file_uploaded']
			try:
				f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))    ##To check if file is existing or not
			except:
				return render_template("index.html", file_msg = "Please upload a file")		
			fm = "uploads/"+f.filename
			

			if fm.endswith(('.mp4','.avi','.mkv')):
				#videofile = open(fm , "rb")  ##open uploaded file
				audiomanager.convert2wav(fm)

				#voskFunction.sttTest(kk)
				op = open("texts_generated/file.srt","w") ##create a subtitle (srt file)
				converted_audio = open("converted.wav","rb")
				stri  = srtImp.transcribe(converted_audio,15)
				op.write(srt.compose(stri))
				op.close()
				converted_audio.close()
				

				stri = srtImp.createText()

				return redirect(url_for("editingPage"))

			else:
				return render_template("index.html", file_msg = "Please upload a video file with extensions '.mp4','.avi','.mkv' ")
			

		elif request.form.get('todo') == 'sensor':
			f = request.files['file_uploaded']
			try:
				f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))    ##To check if file is existing or not
			except:
				return render_template("index.html", file_msg = "Please upload a file")		
			fm = "uploads/"+f.filename
			

			if fm.endswith(('.mp4','.avi','.mkv')):
				#videofile = open(fm , "rb")  ##open uploaded file
				audiomanager.convert2wav(fm)

				#voskFunction.sttTest(kk)
				op = open("texts_generated/file.srt","w") ##create a subtitle (srt file)
				converted_audio = open("converted.wav","rb")
				stri  = srtImp.transcribe(converted_audio,1)
				op.write(srt.compose(stri))
				op.close()
				converted_audio.close()
				stri = srtImp.createText()
				

				

				return redirect(url_for("senSor"))

			else:
				return render_template("index.html", file_msg = "Please upload a video file with extensions '.mp4','.avi','.mkv' ")

		else :
			return render_template("index.html", file_msg = "Please upload a video file with extensions '.mp4','.avi','.mkv'\n and choose any one of the options to proceed ")

						






		
	else:
		
		return render_template("index.html", file_msg = "Please choose a file")		




@app.route("/sensor_page",methods = ["GET", "POST"])
def senSor():

	if request.method == "POST":
		txt_to_sensor = request.form['words_to_filter']
		with open("texts_generated/words_to_filter.txt","w") as f:
			f.write(txt_to_sensor)

		audiomanager.sensorFn()	
		return send_file("new_video.mp4",mimetype='mp4',attachment_filename='video.mp4',as_attachment=True)






	return render_template("sensor_page.html")	








@app.route("/editer" ,methods = ["GET" ,"POST"])
def editingPage():
	#stringEdited = request.form['inputTextToSave']
	file = open("texts_generated/text.txt", 'r')
	readString = file.read()
	file.close()
	

	if request.method == "POST":
		if request.form.get("button1"):
			txt_updated = request.form['inputTextToSave']  ##To retrieve updated text value from text area
			punctuated_file = open("texts_generated/update.txt","w+")
			punctuated_file.write(txt_updated)
			punctuated_file.close()

			demo_play_with_model.punct_function()
			new_file = open("texts_generated/finale.txt","r")
			readString2 = new_file.read()
			new_file.close()
			

			return render_template("editer.html", datastr = readString2, data2 = "Punctuated the text successfully,make your corrections if any")
		elif request.form.get("button2"):

			final_txt = request.form['inputTextToSave']
			file = open("texts_generated/finale.txt","w")

			file.write(final_txt)
			file.close()

			return redirect((url_for("translatingPage")))
			



	return render_template("editer.html" , datastr = readString, data2 = "loaded successfully , check for any word spelling" )




@app.route("/translate" , methods = ["GET" ,"POST"])
def translatingPage():
	file = open("texts_generated/finale.txt","r")
	stringip = file.read()
	file.close()

	text2srt.txt2srt(stringip)

	file_srt = open("texts_generated/final.srt","r")
	string_srt = file_srt.read();

	if request.method == "POST":

		if request.form.get("seg_bt"):
			ip_string = request.form['srt_text']


			
			op_string = text2srt.segment_srt(ip_string)

			

			return render_template("translate.html" , text1 = op_string)
		elif request.form.get("tra_but"):
			val = request.form.get("lang_val")
			with open('texts_generated/lang.txt','w') as f:
				f.write(val)

			txt1 = request.form['srt_text']
			txt2 = text2srt.translate(val,txt1)
		
			return render_template("translate.html",text1 = txt1 ,text2 = txt2)


		elif request.form.get("un_seg"):
			try:
				os.remove('texts_generated/segmented.srt')	
			except IOError:
				print("null")	
			
			with open("texts_generated/final.srt",'r') as fp:
				val = fp.read()

			
			return render_template("translate.html" , text1 = val)
		elif request.form.get("dwld_srt"):
			return send_file("texts_generated/translated_sub.srt",mimetype='srt',attachment_filename='Translated Subtitle.srt',as_attachment=True)
			
		elif request.form.get("proceed"):
			return redirect((url_for("finalPage1")))				 	










	return render_template("translate.html" , text1 = string_srt)



@app.route('/final_page1' , methods = ["GET","POST"])
def finalPage1():
	
	

	if request.method == "POST":
		if request.form.get("vid"):
			audiomanager.makechunks()
			audiomanager.speedupAudio()
			audiomanager.makeVid()
			return send_file("new_video.mp4",mimetype='mp4',attachment_filename='video.mp4',as_attachment=True)
		elif request.form.get("tsub"):
			return send_file("texts_generated/translated_sub.srt",mimetype='srt',attachment_filename='video(translated).srt',as_attachment=True)
		elif request.form.get("osub"):
			try :
				return send_file("texts_generated/segmented.srt",mimetype='srt',attachment_filename='video.srt',as_attachment=True)
			except:
				return send_file("texts_generated/temp.srt",mimetype='srt',attachment_filename='video.srt',as_attachment=True)	
				
				
				









	return render_template("final_page1.html"  , text = "Download your file")








if __name__ == "__main__":
	app.run(debug = True)





