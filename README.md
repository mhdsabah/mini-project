# Machine audio translation for single speaker videos.

## Description 
This project is an application of speech recognition. Users can upload videos,not every kind of videos,paticular videos which has 
single human speaker(like ted talks,speech or presentation) and  the web app will give output with translated 
voice overs in their preffered language.



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
##### Common issues

------------

If there is 'windows file not found ' error , then you need to install ffmpeg. Use this link    [For installing ffmpeg](https://www.youtube.com/watch?v=qjtmgCb8NcE "For installing ffmpeg")



