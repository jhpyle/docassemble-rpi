import RPi.GPIO as GPIO

__all__ = ['set_colors']

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

def set_colors(red=False, green=False):
    if green:
      GPIO.output(23, True)
    else:
      GPIO.output(23, False)
    if red:
      GPIO.output(24, True)
    else:
      GPIO.output(24, False)