# Machine translated voice-over generator for single speaker videos.

## Description 
This project is an application of speech recognition. You will be able to get ouput with trasnlated voice overs in your preffered language for the videos. Does not work with every kind of videos, paticular videos which has **single human speaker** (like ted talks,speech or presentation). 
#### Features
- Uses VOSK open source speech recognition toolkit
- Supports all recognisable language by vosk
- Uses EasyNMT library for translating the textfile
- Works offline 
- Punctutator is used since output from VOSK does not has any punctuation 


------------

## For windows

------------

#### 1. First create a virtual environment
`virtualenv venv`

`.\venv\Script\activate`
#### 2. Clone the github repo to directory 
#### 3. Download following files and place it models folder
[Vosk Model](https://alphacephei.com/vosk/models "Vosk Model") - Choose any English model(for better accuracy:: vosk-model-en-us-aspire-0.2)

[Punctuator model](https://drive.google.com/drive/folders/0B7BsN5f2F1fZQnFsbzJ3TWxxMms "Punctuator model") - Download 'Demo-Europarl-EN.pcl'
#### 4. Using pip
`pip install -r requirements.txt`
#### 5. Start the flask server 
`python first.py`  
  
  
  

------------

## Tools used
- [VOSK](https://alphacephei.com/vosk/ "VOSK")
- [Translator library - EasyNMT](https://pypi.org/project/EasyNMT/ "Translator library - EasyNMT")
- [Ottokart- Punctuator2](https://github.com/ottokart/punctuator2 "Ottokart- Punctuator2")
------------
##### Common issues

------------

- If there is 'windows file not found ' error , then you need to install ffmpeg. Use this link    [For installing ffmpeg](https://www.youtube.com/watch?v=qjtmgCb8NcE "For installing ffmpeg")
- Inorder for translator to work offline you have to download the entire translator file.



