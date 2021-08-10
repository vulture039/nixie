
import threading
from time import sleep

mode = -1

def main():
    thread = threading.Thread(target = mode_edit)
    thread.setDaemon(True)
    thread.start()

    while True:
        print(mode)
        print(threading.get_ident())
        if mode == 1:
            thread = threading.Thread(target = test1)
            thread.setDaemon(True)
            thread.start()
        elif mode == 2:
            thread = threading.Thread(target = test2)
            thread.setDaemon(True)
            thread.start()
        sleep(1)

def test1():
    global mode
    while mode == 1:
        print(threading.get_ident())
        print("test1")
        sleep(1)


def test2():
    global mode
    while mode == 2:
        print(threading.get_ident())
        print("test2")
        sleep(1)
    

def mode_edit():
    global mode
    for i in range(10):
        sleep(5)
        mode += 1

if __name__ == "__main__":
    
    main()