import os
import threading 
import tty
import atexit
import socket
import sys
import time
from datetime import datetime
import pytz
import numpy as np
import pyautogui
import imutils
import cv2
import keyboard

host = ''
port = 9000
speed = 100
locaddr = (host,port)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
sock.bind(locaddr)
trainDir = None

def recv():
    while True:
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break

def sendMsg(msg):
    sent = sock.sendto(msg.encode(encoding="utf-8"), tello_address)
    print("Tello: " + str(sent))

def collectData(key, msg):
    filename = os.path.join(trainDir, key + '-' + datetime.now(pytz.timezone("America/Chicago")).strftime('%Y%m%d%H%M%S%f')[:-3] + ".png")
    img_png = pyautogui.screenshot(region=(2206, 165, 648, 525))
    img_jpg = cv2.cvtColor(np.array(img_png), cv2.COLOR_RGBA2RGB)
    img_adj = cv2.resize(img_jpg, (0,0), fx=.571, fy=.571)
    cv2.imwrite(filename, img_adj)
    sent = sock.sendto(msg.encode(encoding="utf-8"), tello_address)
    print("Tello: " + str(sent))

def key_press(key):
    global speed
    msg = key.name
    if '1' == msg:
        collectData('0','takeoff')
    elif '0' == msg:
        collectData('1', 'land')
    elif 'w' == msg:
        collectData('2', 'up 20')
    elif 's' == msg:
        collectData('3','down 20')
    elif 'a' == msg:
        collectData('4','ccw 90')
    elif 'd' == msg:
        collectData('5','cw 90')
    elif 'up' == msg:
        collectData('6','forward 20')
    elif 'down' == msg:
        collectData('7','back 20')
    elif 'left' == msg:
        collectData('8','left 20')
    elif 'right' == msg:
        collectData('9','right 20')
    elif '=' == msg:
        speed += 10
        sendMsg('speed ' + str(speed))
    elif '-' == msg:
        speed -= 10
        sendMsg('speed ' + str(speed))
    elif 'q' == msg:
        sendMsg('land')
        sock.close()

if __name__ == '__main__':
    # % python train.py folder_name
    if len(sys.argv) < 2:
        print('Usage: python', sys.argv[0], '[training_set_dir]')
        sys.exit(1)
    trainDir = sys.argv[1]
    print ('\r\n\r\nTello is gonna to learn operations.\r\n')
    print ('1: takeoff, 0: land.\r')
    print ('w: up, s: down, a: cccw, d: cw.\r')
    print ('▲: forward, ▼: back, ◀︎: left, ▶︎: right.\r')
    print ('+: speed up, -: speed down.\r')
    print ('This operation will taking photo through drone camera.\r')
    print ('q -- quit demo.\r\n')

    #recvThread create
    recvThread = threading.Thread(target=recv)
    recvThread.start()
    sock.sendto('command'.encode(encoding="utf-8"), tello_address)

    # keyboard monitering
    keyboard.on_press(key_press)