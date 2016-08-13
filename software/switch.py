import RPi.GPIO as GPIO
import time
import pygame
import random
import glob
import datetime
import mutagen
import vlc

#mutagen library is used for reading mp3 file length
#(if someone know how to do it with vlc library please let me know)
from mutagen.mp3 import MP3
from mutagen.mp3 import MPEGInfo

#button is connected to GPIO pin 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#directory where mp3 files are stored (on flash drive)
DIR = "/media/pi/KINGSTON/poems/*.mp3"

#setting the output
#(USB speakers are used)
instance = vlc.Instance('--aout=alsa')

player = instance.media_player_new()

#message after initialization
print("Versostroj is ready.")

#endless loop
while True:
	input_state = GPIO.input(18)
	if input_state == False:
		print('Button Pressed')

		poemsList = glob.glob(DIR)
		count = len(poemsList)
		print("Poems count: " + str(count))

		n = random.randint(1, count)
		print("Will be played: " + poemsList[n - 1])
		
		media = instance.media_new(poemsList[n - 1])		
		player.set_media(media)
		player.play()			
                                
        	audio = MP3(poemsList[n - 1])                		
		time.sleep(audio.info.length)		

		#logging to log.txt file
		timeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		with open("./log.txt", "a") as logfile:
			logfile.write(timeNow + " " + poemsList[n - 1] + "\n")

		print("Finished. Ready for next poem.")
