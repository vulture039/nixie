# coding: UTF-8

import threading
import datetime
import serial
import RPi.GPIO as gpio
import io
import requests
import pandas as pd
import numpy
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
    if mode < 2:
        mode += 1
    else:
        mode = 0

#     sleep(1)

    # モードに応じて呼び出す
    if mode == 0:
        thread = threading.Thread(target = test)
    elif mode == 1:
        thread = threading.Thread(target = get_current_time)
    elif mode == 2:
        thread = threading.Thread(target = COVID19_newly_confirmed_cases_in_tokyo)
    else:
        return
    thread.setDaemon(True)
    thread.start()

def test():
    global current_time
    global mode
    
    current_time = ["R", "R", "R", "R", "R", "R", "R", "R", "\n"]
    digit = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "R", "L"]

    while mode == 0:
        for c in digit:
            if mode != 0:
                break
            current_time[6] = c
            print(current_time)
            sleep(0.5)

def get_current_time():
    global current_time
    global mode

    while mode == 1:
        dt_now = datetime.datetime.now()
        current_time = list(dt_now.strftime('%H%M%S'))
        current_time.insert(2,"R")
        current_time.insert(5,"R")
        current_time.insert(8,"\n")
        print(current_time)
        sleep(0.5)

def COVID19_newly_confirmed_cases_in_tokyo():
    global current_time
    global mode

    url = 'https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv'
    res = requests.get(url)
    df = pd.read_csv(io.BytesIO(res.content), sep=",")
    latest_value = df[df['Prefecture'] == 'Tokyo'].tail(1).values
    date = latest_value[0][0]
    cases = latest_value[0][2]
    data = list(str(cases))
    current_time = numpy.pad(data, [8-len(data),0], 'constant', constant_values=('N')).tolist()
    current_time.append("\n")
    print(latest_value)

    while mode == 2:
        print(current_time)
        sleep(0.5)

def serial_send():
    ser = serial.Serial('/dev/ttyAMA0',57600) # 115200

    while True:
        ser.write(current_time)
        #print("write")
        sleep(0.5)

    ser.close()

if __name__ == "__main__":
    main()
