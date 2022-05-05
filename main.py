# Multiprocssing for running multiple functions parallely
# Corey Schafer Multiprocessing: https://www.youtube.com/watch?v=fKl2JW_qrso
# https://docs.python.org/3/library/multiprocessing.html

import time, multiprocessing as mp # Python's libraries
import keylogger, face_detection # My libraries

def fun():
    while True:
        print("fun!")
        time.sleep(.5)

# For a complicated explanation of why the if __name__ == '__main__' part
# is necessary for multiprocessing, see this: 
# https://docs.python.org/3/library/multiprocessing.html#multiprocessing-programming
if __name__ == "__main__":

    # create a process
    p1 = mp.Process(target=keylogger.log_keys)
    p2 = mp.Process(target=fun)
    p3 = mp.Process(target=face_detection.face_monitoring)

    # start that process
    p1.start()
    p2.start()
    p3.start()

    # make the script wait for the process to terminate before the script ends
    p1.join()
    p2.join()
    p3.join()


