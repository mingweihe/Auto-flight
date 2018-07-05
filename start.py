# coding: utf-8

# In[1]:
import numpy as np
import pyautogui
import cv2
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=FutureWarning)
    import tensorflow as tf
import threading
import os
import termios
import tty
import atexit
import socket
import sys
import time
import keyboard

host = ''
port = 9000
locaddr = (host,port) 

signalCheckPeriod = 1 # seconds
autoFlyCheckPeriod = 10

#emergency check
emergencyLand = 0

test = 0

# environment variables, prevent warning infor from tensorflow which caused by GPU
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


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

def sendMsg(msg):
    if 0 == msg:
        msg = 'takeoff'
    elif 1 == msg:
        msg = 'land'
    elif 2 == msg:
        msg = 'up 20'
    elif 3 == msg:
        msg = 'down 20'
    elif 4 == msg:
        msg = 'cw 90'
    elif 5 == msg:
        msg = 'ccw 90'
    elif 6 == msg:
        msg = 'forward 20'
    elif 7 == msg:
        msg = 'back 20'
    elif 8 == msg:
        msg = 'left 20'
    elif 9 == msg:
        msg = 'right 20'
    else:
        msg = None
    if msg is None:
        return
    print(msg)
    sent = sock.sendto(msg.encode(encoding="utf-8"), tello_address)
    print("Tello: ", str(sent))

def signalMode(gestureSession, prediction):
    global emergencyLand
    if not emergencyLand and not gestureSession._closed:
        img_png = pyautogui.screenshot(region=(2206, 165, 648, 525))
        img_jpg = cv2.cvtColor(np.array(img_png), cv2.COLOR_RGBA2RGB)
        img_adj = cv2.resize(img_jpg, (0,0), fx=.571, fy=.571)

        output = gestureSession.run(prediction, feed_dict = {img_holder: [img_adj], train:False})
        print("prediction:", output[0])
        # take off
        # our test set is friendly for classifier(40epochs15k+) 2 and 4, so we change a little bit of the message.
        if output[0] == 2:
            sendMsg(0)
        # land
        elif output[0] == 4:
            sendMsg(1)
        # autofly
        elif output[0] == 3:
            signalModelInitialize()
            return
        
        #Video analysize Thread
        threading.Timer(signalCheckPeriod, signalMode, [gestureSession, prediction]).start()

def signalModelInitialize():
    print()
    print('intelligent flight mode is launching...')
    print("Automatic flying data is initializing...")
    sess.close()
    # restore checkpoint
    sessOpt = tf.Session()
    saverOpt = tf.train.import_meta_graph(os.path.join(OPERATION_CHECKPOINTS_DIR, 'model.meta'))
    saverOpt.restore(sessOpt, tf.train.latest_checkpoint(OPERATION_CHECKPOINTS_DIR))
    predOpt = sessOpt.graph.get_tensor_by_name('prediction:0')
    img_holder_opt = sessOpt.graph.get_tensor_by_name('image_holder:0')
    print("Automatic flying data initialization is complte")
    print('intelligent flight mode has been successfully lauched')
    print()
    intelligentMode(sessOpt, predOpt, img_holder_opt)

def intelligentMode(sessOpt, predOpt, img_holder_opt):
    global emergencyLand
    if not emergencyLand and not sessOpt._closed:
        img_png = pyautogui.screenshot(region=(2206, 165, 648, 525))
        img_jpg = cv2.cvtColor(np.array(img_png), cv2.COLOR_RGBA2GRAY)
        img_adj = cv2.resize(img_jpg, (0,0), fx=.571, fy=.571)

        output = sessOpt.run(predOpt, feed_dict = {img_holder_opt: [np.reshape(img_adj, [-1])]})[0]
        print("prediction:", output)
        sendMsg(output)
        threading.Timer(autoFlyCheckPeriod, intelligentMode, [sessOpt, predOpt, img_holder_opt]).start()

def key_press(key):
    global emergencyLand
    if "alt" == key.name:
        signalModelInitialize()
    if "right option" == key.name:
        emergencyLand = 1
        sendMsg(1)
        sock.close()

if __name__ == '__main__':
    # % python train.py folder_name
    if len(sys.argv) < 3:
        print('Usage: python', sys.argv[0], '[gesture_checkpoints_dir] [opeartion_checkpoints_dir]')
        sys.exit(1)

    IMAGE_HEIGHT = 300
    IMAGE_WIDTH = 370
    GESTURE_CHECKPOINTS_DIR = sys.argv[1]
    OPERATION_CHECKPOINTS_DIR = sys.argv[2]

    # Gesture recognition graph preparation:
    print()
    print("Gesture recognition is initializing...")
    sess = tf.Session()
    saver = tf.train.import_meta_graph(os.path.join(GESTURE_CHECKPOINTS_DIR, 'model.meta'))
    saver.restore(sess, tf.train.latest_checkpoint(GESTURE_CHECKPOINTS_DIR))

    # restore tensors
    img_holder = sess.graph.get_tensor_by_name('img_holder:0')
    lbl_holder =sess.graph.get_tensor_by_name('lbl_holder:0')
    train = sess.graph.get_tensor_by_name('train_bool:0')
    predict = sess.graph.get_tensor_by_name('prediction:0')
    probabilities = sess.graph.get_tensor_by_name('probabilities:0')
    print("Gesture recognition initialization is complete")
    keyboard.on_press(key_press)
    print("Emergency protection launch is complete")
    print("Ready to fly:")
    print()
    #connect to tello and ask for command
    sock.sendto('command'.encode(encoding="utf-8"), tello_address)

    #recvThread create
    threading.Thread(target=recv).start()

    #Video analysize Thread
    signalMode(sess, predict)

    # In[7]:
    # sess.close()

