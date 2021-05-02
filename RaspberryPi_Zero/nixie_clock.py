# coding: UTF-8

import threading
import datetime
import serial
import RPi.GPIO as gpio
from time import sleep

current_time = []
pin = 18
mode = -1

def main():
    serial_thread = threading.Thread(target = serial_send)
    serial_thread.setDaemon(True)
    serial_thread.start()

    try:
        gpio.setmode(gpio.BCM)
        gpio.setup(pin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        while True:
            if not 'event' in locals():
                event = gpio.add_event_detect(pin, gpio.RISING, callback=on_push, bouncetime=200)
            else:
                print(mode)
                sleep(1)
    finally:
        gpio.cleanup()
        serial_thread.join(1)

def on_push(channel):
    global mode
    print ("Button Pushed.")
    if mode != -1:
        thread.stop()
    if mode < 1:
        mode += 1
    else:
        mode = 0
    # モードに応じて呼び出す
    thread = MyThread(mode)
    thread.start()

class MyThread(threading.Thread):
    def __init__(self, i):
        super(MyThread, self).__init__()
        self.i = i
        self.stop_event = threading.Event()
        self.setDaemon(True)
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        print ('START {}'.format(self.i))
        while not self.stop_event.is_set():
            if self.i == 0:
                test()
            elif self.i == 1:
                get_current_time()
            time.sleep(0.5)

def test():
    global current_time
    
    current_time =["R", "R", "R", "R", "R", "R", "R", "R", "\n"]
    digit = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "R", "L"]

    for c in digit:
        current_time[6] = c
        print(current_time)

def get_current_time():
    global current_time

    dt_now = datetime.datetime.now()
    current_time = list(dt_now.strftime('%H%M%S'))
    current_time.insert(2,"R")
    current_time.insert(5,"R")
    current_time.insert(8,"\n")
    print(current_time)

def serial_send():
    ser = serial.Serial('/dev/ttyAMA0',57600) # 115200

    while True:
        ser.write(current_time)
        #print("write")
        sleep(0.5)

    ser.close()

if __name__ == "__main__":
    main()
