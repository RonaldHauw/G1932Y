import pygame
import time
from threading import Thread


def play():
    pygame.mixer.init()
    pygame.mixer.music.load("Morningbirds.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue



p1 = Thread(target=play)
p1.start()
print "yolo"
time.sleep(2)
print "shutting down"
pygame.mixer.music.stop()
