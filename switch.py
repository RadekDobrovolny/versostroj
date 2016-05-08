import RPi.GPIO as GPIO
import time
import pygame
import random

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(18)
    if input_state == False:
        print('Button Pressed')
        pygame.mixer.init()
        pygame.mixer.music.load("1.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        time.sleep(0.2)



