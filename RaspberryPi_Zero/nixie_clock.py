import threading
import datetime
import serial
from time import sleep

current_time = []

def main():
    
    time_thread = threading.Thread(target = get_current_time)
    time_thread.setDaemon(True)
    time_thread.start()
    """
    test_thread = threading.Thread(target = test)
    test_thread.setDaemon(True)
    test_thread.start()
    """

    sleep(1)

    serial_thread = threading.Thread(target = serial_send)
    serial_thread.setDaemon(True)
    serial_thread.start()

    while True:
        #print("running")
        serial_thread.join(1)

def test():
    global current_time
    i = 0
    current_time =["R", "R", "R", "R", "R", "R", "R", "R", "\n"]
    digit = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "R", "L"]


    while True:
        for c in digit:
            current_time[6] = c
            print(current_time)
            sleep(1)  

def get_current_time():
    global current_time
    i = 0

    while True:
        
        dt_now = datetime.datetime.now()
        current_time = list(dt_now.strftime('%H%M%S'))
        current_time.insert(2,"R")
        current_time.insert(5,"R")
        current_time.insert(8,"\n")
        print(current_time)
        sleep(0.5)
        """
        current_time_int=[0,1,2,3,4,5,6,7]
        current_time_int[7] = i
        current_time = [str(n) for n in current_time_int]
        current_time.insert(8,"\n")
        #current_time = "".join(current_time)
        if i > 8:
            i = 0
        else:
            i += 1
        print(current_time)
        sleep(1)
        """

def serial_send():
    ser = serial.Serial('/dev/ttyAMA0',57600)# 57600)#115200

    while True:
        ser.write(current_time)
        #print("write")
        sleep(0.5)

    ser.close()

if __name__ == "__main__":
    main()
