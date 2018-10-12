import pygame
from pygame.locals import *
import sys
import random
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

TRIGGER = 18
ECHO = 23

GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setwarnings(False)

class FlappyBird:
    dis = 10
    temp = 0
    diss = 3
   

    def distance(self):
        distance = 0
        GPIO.output(TRIGGER, True)
 
        time.sleep(0.00001)
        GPIO.output(TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

   
        while GPIO.input(ECHO) == 0:
            StartTime = time.time()

   
        while GPIO.input(ECHO) == 1:
            StopTime = time.time()

   
        TimeElapsed = StopTime - StartTime
   
        distance = int(TimeElapsed * 34300 / 2)
     
        if 5 < distance < 88:
          self.dis = distance
          return distance
        else:
            return self.dis
         
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 708))
        self.bird = pygame.Rect(60, 50, 50, 50)
        self.background = pygame.image.load("assets/background.png").convert()
        self.birdSprites = [pygame.image.load("assets/1.png").convert_alpha(),
                            pygame.image.load("assets/2.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = 130
        self.wallx = 400
        self.birdY = 350
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)

    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400
            self.counter += 1
            self.offset = random.randint(-110, 110)

    def birdUpdate(self):
        self.temp = self.distance() * 1
       
        if self.temp >= self.diss:
          if self.temp - self.diss <= 3:
              self.diss = self.temp
              self.birdY = 700 - self.temp * 8
        elif self.diss > self.temp:
          if self.diss - self.temp <= 3:
              self.diss = self.temp
              self.birdY = 700 - self.temp * 8
        else:
            self.birdY = 700 - self.diss * 8

        self.bird[1] = self.birdY
       
        upRect = pygame.Rect(self.wallx,
                            360 + self.gap - self.offset + 10,
                            self.wallUp.get_width() - 10,
                            self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                              0 - self.gap - self.offset - 10,
                              self.wallDown.get_width() - 10,
                              self.wallDown.get_height())
        if upRect.colliderect(self.bird):
            self.dead = True
        if downRect.colliderect(self.bird):
            self.dead = True
        if not 0 < self.bird[1] < 720:
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 400
            self.offset = random.randint(-110, 110)
            self.gravity = 5

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
               
                 

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp,
                            (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown,
                            (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.counter),
                                        -1,
                                        (255, 255, 255)),
                            (200, 50))
            self.sprite = 0
            if self.dead:
                self.sprite = 2
            self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
            if not self.dead:
                self.sprite = 0
                self.updateWalls()
                self.birdUpdate()
                pygame.display.update()

if __name__ == "__main__":
    FlappyBird().run()
