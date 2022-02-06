import glob
import logging
import pygame
import random
import RPi.GPIO as GPIO
import sys
import time
from mutagen.mp3 import MP3

# GPIO pins for LED matrix
HOR0 = 23
HOR1 = 24
HOR2 = 25

VER0 = 11
VER1 = 9
VER2 = 10
VER3 = 22
VER4 = 21
VER5 = 17
VER6 = 4

# GPIO pin for button
BUTTON = 18

horizontal = [HOR0, HOR1, HOR2]
vertical = [VER0, VER1, VER2, VER3, VER4, VER5, VER6]

# folder where MP3 files are stored (eg. on flash drive)
DIR = "/home/versostroj/software/poems/*.mp3"


def init_leds():
    vertical.reverse()
    for pin in horizontal + vertical:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
    leds_up()


def leds_down():
    # turn-off all LEDs
    for pin in horizontal + vertical:
        GPIO.output(pin, GPIO.HIGH)


def leds_up():
    # turn-on single LED columns one by one
    for column in vertical:
        for p in vertical:
            if p is not column:
                GPIO.output(p, GPIO.HIGH)
            else:
                GPIO.output(p, GPIO.LOW)
        time.sleep(0.15)

    # turn-on whole LED matrix adding columns
    vertical.reverse()
    for column in vertical[1:]:
        GPIO.output(column, GPIO.LOW)
        time.sleep(0.15)
    vertical.reverse()


def leds_shade_down():
    # turn-off LED matrix column by column
    vertical.reverse()
    for column in vertical:
        GPIO.output(column, GPIO.HIGH)
        time.sleep(0.15)
    vertical.reverse()


def init_versostroj():
    # setting environment and turn-on LEDs
    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s %(message)s',
                        datefmt='%d. %m. %Y %I.%M:',
                        level='INFO')

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    pygame.init()
    pygame.mixer.init()
    init_leds()
    logging.info("Versostroj is ready.")


def loop():
    last_five = [None, None, None, None, None]  # list for last 5 played poems
    while True:
        if not GPIO.input(BUTTON):
            logging.info('Button pressed.')

            poems_list = glob.glob(DIR)

            if len(poems_list) <= 5:
                logging.error(f'Sorry, not enough poems in directory. Only {len(poems_list)} was found. '
                              f'Please add some MP3 files.')
                continue

            while True:
                file = random.choice(poems_list)
                logging.info(f"Random pick: {file}")
                if file not in last_five:
                    last_five.append(file)
                    last_five.pop(0)
                    break
                logging.info(f"It seems {file} played recently. I am about to try another pick.")

            audio = MP3(file)  # mutagen
            poem_len = audio.info.length * 1000  # length of MP3 file in milliseconds

            pygame.mixer.music.load(file)
            pygame.mixer.music.play()

            leds_shade_down()

            step = 1  # steps for showing progress on LED matrix
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                position = float(pygame.mixer.music.get_pos()) / poem_len * 100
                if position > step * (100 / 8):
                    if step in range(1, 8):
                        GPIO.output(vertical[step - 1], GPIO.LOW)
                    step += 1

            logging.info("Playback finished. Ready for next poem.")


def main():
    init_versostroj()
    loop()


if __name__ == "__main__":
    main()
