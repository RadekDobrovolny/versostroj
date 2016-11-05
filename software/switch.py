import RPi.GPIO as GPIO
import time
import pygame
import random
import glob
import datetime

# Button is connected to GPIO pin 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Directory where mp3 files are stored (on flash drive)
DIR = "/media/pi/KINGSTON/Versostroj/*.mp3"

pygame.mixer.init()

print("Versostroj is ready.")

while True:
	input_state = GPIO.input(18)
	if input_state == False:
		print('Button Pressed')

		poemsList = glob.glob(DIR)
		count = len(poemsList)
		print("Poems count: " + str(count))

		n = random.randint(1, count)
		print("Will be played: " + poemsList[n - 1])

		pygame.mixer.music.load(poemsList[n - 1])
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy() == True:
			continue
		time.sleep(0.2)

		#logging to log.txt file
		timeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		with open("/media/pi/KINGSTON/Log/log.txt", "a") as logfile:
			logfile.write(timeNow + " " + poemsList[n - 1] + "\n")

		print("Finished. Ready for next poem.")
