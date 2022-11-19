import time
time.sleep(10)
from vosk import Model, KaldiRecognizer
import traceback
import pyaudio
import pyautogui
import pyrebase
import pywhatkit
import mouseinfo
import os
import sys
from firebase import firebase


if os.environ.get('DISPLAY','') == '':
	print('no display found. Using :0.0')
	os.environ.__setitem__('DISPLAY', ':0.0')



config = {
  "apiKey": "AIzaSyCBMoMS-zz_Ji0sJ169IysHVqH8bVHHWs8",
  "authDomain": "smart-home-db-80bd0.firebaseapp.com",
  "databaseURL": "https://smart-home-db-80bd0-default-rtdb.europe-west1.firebasedatabase.app/",
  "storageBucket": "smart-home-db-80bd0.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db=firebase.database()
#db.child("switches").child("0").update({"state":1})

model=Model(r"/home/pi/vosk-model-small-en-in-0.4")
db.child("switches").child("0").update({"state":1})
#time.sleep(2)
recognizer=KaldiRecognizer(model,44100)

db.child("switches").child("0").update({"state":2})
#time.sleep(2)

mic=pyaudio.PyAudio()

db.child("switches").child("0").update({"state":3})
#time.sleep(2)
try:
	db.child("switches").child("0").update({"state":2})
	#time.sleep(2)
	print("gfcgfch")
	h=open("/home/pi/finale/tryblock.txt","a")
	h.write("aaaaaaaaaaaa")
	h.close()
	mic.devrate=int(mic.get_device_info_by_index(mic.devindex).get('defaultSampleRate'))
	stream=mic.open(format=pyaudio.paInt16,channels=1,rate=mic.devrate,input_device_index=mic.devindex,input=True,frames_per_buffer=mic.chunk,stream_callback=mic.processor.ReadCallback)
	stream.start_stream()

except Exception as e:
	print("hgyuydfggdtyuh")
	#traceback.print_exc()
	print("hjgbchgfduity")
	print(str(e))
	f = open("/home/pi/finale/err.txt", "a")
	f.write(str(e))
	f.close()
	g= open("/home/pi/finale/terr.txt", "a")
	g.write("wekjfvhwhefbvkwhf")
	g.close()
	print("success")


db.child("switches").child("0").update({"state":4})
time.sleep(2)

#stream.start_stream()
db.child("switches").child("0").update({"state":5})
time.sleep(2)

#db.child("switches").child("0").update({"err":e})

#db.child("switches").child("0").update({"state":0})
#time.sleep(2)

while True:
	#db.child("switches").child("0").update({"state":0})
	#time.sleep(4)
	data=stream.read(4096)
	if recognizer.AcceptWaveform(data):
		#db.child("switches").child("0").update({"state":1})
		#time.sleep(4)
		text=recognizer.Result()
		buffer=text[14:-3]
		result=buffer.lower()
		print("I heard: ", result)
		if "bob" in result:
			result=result.replace("bob","")
			print("detected bob")
			if (("on" in result) and ("ght" in result)):
				print("Turning the light on")
				db.child("switches").child("0").update({"state":1})
				db.child("switches").child("0").update({"automation_value": 255})
			elif ("ght" in result and ("of" in result or "off" in result)):
				db.child("switches").child("0").update({"state":0})
				db.child("switches").child("0").update({"automation_value":0})
				print("Turning the light off")
			elif ("ght" in result and "dim" in result):
				db.child("switches").child("0").update({"automation_value": 64})
				print("Dimming the light")
			elif "fan" in result and "on" in result:
				db.child("switches").child("2").update({"state":1})
				print("Turning the fan on")
			elif "fan" in result and "of" in result:
				db.child("switches").child("2").update({"state":0})
				print("Turning the fan off")
#			else:
#				print(result)

		print(result)
