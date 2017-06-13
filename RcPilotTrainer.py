# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import random
import copy
from operator import attrgetter
import config
# import numpy as np
# import quaternion

# IMPORT OBJECT LOADER
from objloader import *


config = config.Config()
config.showDialog()

pygame.init()
viewport = (1000,800)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

pygame.joystick.init()
print "Joystick ",
joystick = None
if pygame.joystick.get_count():
    print "FOUND"
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    print "NOT FOUND"
    exit(1)

glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

# LOAD OBJECT AFTER PYGAME INIT
obj = OBJ("cessna.obj", swapyz=True)

clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)


def doFreeMotion():
    
    glLoadIdentity()
    glTranslate(0, 0, -8) 
    glRotate(-90, 1, 0, 0) 
    glPushMatrix()
        
    rot = [-90,0,0]
    while True:
        clock.tick(30)
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                sys.exit()
                
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPopMatrix()

        for inputChannel, axis in ((0,1), (1,0), (5, 2)):
            input = joystick.get_axis(inputChannel)
            if input < -.1 or input > .1: glRotate(input*4, 1 if axis==0 else 0, 1 if axis==1 else 0, 1 if axis==2 else 0)
                
        glPushMatrix()
        
        glCallList(obj.gl_list)
        pygame.display.flip()
 
TESTRES_OK = 1
TESTREF_HESITATED = 2
TESTRES_FAIL = 2       

def doTest(test):
    
    STATE_WAITING = 1
    STATE_TESTING = 2
    STATE_COMPLETED = 3
    
    state = STATE_WAITING
    
    glClearColor(0, 0, 0, 0.0) 
    
    glLoadIdentity()
    glTranslate(0, 0, -8) 
    glRotate(-90, 1, 0, 0) 
    glRotate(test.startPos[0], 1, 0, 0)
    glRotate(test.startPos[1], 0, 1, 0)
    glRotate(test.startPos[2], 0, 0, 1)
    
    glPushMatrix()
    
    startTime = time.time()
        
    while True:
        clock.tick(30)
        
        runtime = time.time()-startTime
        
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                sys.exit()
                
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPopMatrix()
        
        rot = [0.0,0.0,0.0]
        
        if state == STATE_TESTING:
            for i in range(3): rot[i] += test.rotation[i] 
           
        joystickInput = False 
        for inputChannel, axis in ((0,1), (1,0), (5, 2)):
            input = joystick.get_axis(inputChannel)
            if input < -.1 or input > .1: 
                rot[axis] += input *5
                joystickInput = True
            
        glRotate(rot[0], 1, 0, 0)
        glRotate(rot[1], 0, 1, 0)
        glRotate(rot[2], 0, 0, 1)
                
        glPushMatrix()
        
        glCallList(obj.gl_list)
        pygame.display.flip()
        
        maxRot = max(map(abs, rot))
        
        if state == STATE_TESTING:
            if maxRot < .3:
                pygame.mixer.music.load('success.wav')
                pygame.mixer.music.play()
                state = STATE_COMPLETED
                if runtime < 4:
                    glClearColor(0,1,0,0)
                    test.nbSuccess += 1
                    result = TESTRES_OK
                else:
                    glClearColor(1,1,0,0)
                    test.nbFail += 1
                    result = TESTREF_HESITATED
            
            if runtime > 15 or maxRot > 1:
                pygame.mixer.music.load('fail.wav')
                pygame.mixer.music.play()
                state = STATE_COMPLETED
                glClearColor(1,0,0,0)
                test.nbFail += 1
                result = TESTRES_FAIL
            
        if state == STATE_WAITING and runtime > 1: state = STATE_TESTING
        
        if state == STATE_COMPLETED and joystickInput == False:
            if not pygame.mixer.music.get_busy():    
                glPopMatrix()
                time.sleep(1)
                return result
    
    

def genStartPosFlatFlight():
    angle = random.randrange(0, 360, 45)
    return (0, 0, angle)

def genStartPosReversedFlight():
    angle = random.randrange(0, 360, 45)
    return (180, 0, angle)

def genStartPosStraightUp():
    angle = random.randrange(0, 360, 45)
    return (90, angle, 0)
    
def genRotationAilerons():
    rot = 1 if random.randrange(2) else -1
    return [0, rot, 0]

def genRotationElev():
    rot = 1 if random.randrange(2) else -1
    return [rot, 0, 0]

def genRotationRudder():
    rot = 1 if random.randrange(2) else -1
    return [0, 0, rot]


class Test(object):
    
    def __init__(self, startPos, rotation):
        self.startPos = copy.copy(startPos)
        self.rotation = copy.copy(rotation)
        self.nbSuccess = 0
        self.nbFail = 0
        
    def getNbTests(self):
        return self.nbSuccess + self.nbFail
        
    def getSuccessRate(self):
        nbTests = self.getNbTests()
        if nbTests > 0:
            return float(self.nbSuccess)/(self.nbSuccess+self.nbFail)
        else:
            return 0
        
    def getConfidence(self):
        return self.getSuccessRate() * (self.nbSuccess+5)
        
        
    def __str__(self):
        return "Pos %15s Rot %10s nbSuccess:%2d nbFail:%2d successRate:%3d%% conf:%2.2f" % (str(self.startPos), str(self.rotation), self.nbSuccess, self.nbFail, self.getSuccessRate()*100, self.getConfidence())



startPosOptions = (genStartPosFlatFlight, genStartPosReversedFlight, genStartPosStraightUp)
rotationOptions = (genRotationAilerons, genRotationElev, genRotationRudder)

print "Preparing Tests"
tests = []
# for i in range(25):
#     startPos = startPosOptions[random.randrange(len(startPosOptions))]()
#     rotation = rotationOptions[random.randrange(len(rotationOptions))]() 
#     tests.append(Test(startPos, rotation))

def genTests(startPos, startPosAngleAxis, startPosAngleSteps, rotAxises):
    res = []
    for rotAxis in rotAxises:
        for angle in startPosAngleSteps:
            start = [x for x in startPos]
            start[startPosAngleAxis] += angle 
            rot = [0,0,0]
            rot[rotAxis] = 1
            res.append(Test(start, rot))
            rot[rotAxis] = -1
            res.append(Test(start, rot))
    return res

AXIS_ELEV = 0
AXIS_AIL = 1
AXIS_YAW = 2

POS_FLYAWAY = (0,0,0)
POS_FLYAWAY_INV = (0,180,0)
POS_STRAIGHTUP = (90,0,0)
POS_STRAIGHTDOWN = (-90,0,0)
POS_KNIFEEDGE_L = (90,0,90)
POS_KNIFEEDGE_R = (90,0,-90)

rotAxises =[]
if config.Aileron:      rotAxises.append(AXIS_AIL)
if config.Elevator:     rotAxises.append(AXIS_ELEV)
if config.Yaw:          rotAxises.append(AXIS_YAW)

if config.Flat:         tests += genTests(POS_FLYAWAY,      AXIS_YAW,   range(0,360,45),    rotAxises)
if config.Inverted:     tests += genTests(POS_FLYAWAY_INV,  AXIS_YAW,   range(0,360,45),    rotAxises)
if config.StraightUp:   tests += genTests(POS_STRAIGHTUP,   AXIS_AIL,   range(0,360,45),    rotAxises)
if config.StraightDown: tests += genTests(POS_STRAIGHTDOWN, AXIS_AIL,   range(0,360,45),    rotAxises)
if config.KnifeEdge:    
                        tests += genTests(POS_KNIFEEDGE_L,    AXIS_YAW,   range(0,360,180),   rotAxises)
                        tests += genTests(POS_KNIFEEDGE_R,    AXIS_YAW,   range(0,360,180),   rotAxises)
    
random.shuffle(tests)
                 
while True:
    
    tests.sort(key=Test.getConfidence)
    print "\nSorted tests"
    for test in tests:
        print " ", str(test)
    #test = tests[random.randrange(len(tests))]
    test = tests[0]
    res = doTest(test)
#     while True:
#         res = doTest(test)
#         if res == TESTRES_OK:
#             break
