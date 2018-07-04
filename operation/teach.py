#
# Tello Python3 Control Demo 
#
# http://www.ryzerobotics.com/
#
# 1/1/2018

import os
import threading 
import termios
import tty
import atexit
import socket
import sys
import time


host = ''
port = 9000
speed = 100
locaddr = (host,port) 


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tello_address = ('192.168.10.1', 8889)

sock.bind(locaddr)

def recv():
    count = 0
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break

def getKey():
   fd = sys.stdin.fileno()
   old = termios.tcgetattr(fd)
   new = termios.tcgetattr(fd)
   new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
   new[6][termios.VMIN] = 1
   new[6][termios.VTIME] = 0
   termios.tcsetattr(fd, termios.TCSANOW, new)
   key = None
   try:
      key = os.read(fd, 3)
   finally:
      termios.tcsetattr(fd, termios.TCSAFLUSH, old)
   return key

from datetime import datetime
import pytz
import numpy as np
import pyautogui
import imutils
import cv2

def collectData(key, msg):
    filename = "/Users/hemingwei/Documents/MUM/ML/project/AutoFlight/data/operation/training_data/" + key + \
        "-" + datetime.now(pytz.timezone("America/Chicago")).strftime('%Y%m%d%H%M%S%f')[:-3] + ".png"
    img_png = pyautogui.screenshot(region=(2206, 165, 648, 525))
    img_jpg = cv2.cvtColor(np.array(img_png), cv2.COLOR_RGBA2RGB)
    img_adj = cv2.resize(img_jpg, (0,0), fx=.571, fy=.571)
    cv2.imwrite(filename, img_adj)
    sent = sock.sendto(msg.encode(encoding="utf-8"), tello_address)
    print("Tello: " + str(sent))

print ('\r\n\r\nTello is gonna to learn operations.\r\n')
print ('Space Key -- Ready to study.\r')
print ('1: takeoff, 0: land.\r')
print ('w: up, s: down, a: cw, d: ccw.\r')
print ('▲: forward, ▼: back, ◀︎: left, ▶︎: right.\r')
print ('+: speed up, -: speed down.\r')
print ('This operation will taking photo through drone camera.\r')
print ('q -- quit demo.\r\n')


#recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()

while True: 

    try:
        #msg = input("");
        msg=str(getKey())
        if not msg:
            break  

        if "b'q'" == msg:
            print ('...')
            sock.close()  
            break

        # operation dispatching
        if "b'1'" == msg:
            collectData('0','takeoff')
        elif "b'0'" == msg:
            collectData('1', 'land')
        elif "b'w'" == msg:
            collectData('2', 'up 20')
        elif "b's'" == msg:
            collectData('3','down 20')
        elif "b'a'" == msg:
            collectData('4','cw 90')
        elif "b'd'" == msg:
            collectData('5','ccw 90')
        elif "b'\\x1b[A'" == msg:
            collectData('6','forward 20')
        elif "b'\\x1b[B'" == msg:
            collectData('7','back 20')
        elif "b'\\x1b[D'" == msg:
            collectData('8','left 20')
        elif "b'\\x1b[C'" == msg:
            collectData('9','right 20')
        elif "b'='" == msg:
            speed += 10
            sock.sendto(('speed ' + str(speed)).encode(encoding="utf-8"), tello_address)
        elif "b'-'" == msg:
            speed -= 10
            sock.sendto(('speed ' + str(speed)).encode(encoding="utf-8"), tello_address)
        elif "b' '" == msg:
            sock.sendto('command'.encode(encoding="utf-8"), tello_address)
        else:
            print("operation not found")

    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()  
        break




