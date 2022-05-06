# To activate venv: venv\Scripts\activate.bat

# Multiprocssing for running multiple functions parallely
# Corey Schafer Multiprocessing: https://www.youtube.com/watch?v=fKl2JW_qrso
# https://docs.python.org/3/library/multiprocessing.html

import multiprocessing as mp, sys, time # Python's libraries
import keylogger, face_detection, window_monitor, pc_locker # My libraries

def all_processes_alive(list_of_processes):
    for p in list_of_processes:
        time.sleep(0.5)
        print("process is alive?", p.is_alive())
        if not p.is_alive():
            print("returning False")
            return False
    print("returning True")    
    return True

def kill_all_processes(list_of_processes):
    print("killing all processes!")
    for p in list_of_processes:
        p.terminate() # terminate is like "shut down", kill is like "turn off switch" | https://stackoverflow.com/a/19206399/11684146

# For a complicated explanation of why the if __name__ == '__main__' part
# is necessary for multiprocessing, see this: 
# https://docs.python.org/3/library/multiprocessing.html#multiprocessing-programming
if __name__ == "__main__":

    # create a process
    p1 = mp.Process(target=keylogger.log_keys)
    exactly_allowed_titles=[]; partially_allowed_titles=['Code', 'Brave']
    p2 = mp.Process(target=window_monitor.check_illegal_window, args=(exactly_allowed_titles, partially_allowed_titles))
    p3 = mp.Process(target=face_detection.face_monitoring)

    # set process as daemon to allow the process to run in the background
    # by settting it as daemon, Python will not run p.join() implicitly
    p1.daemon = True
    p2.daemon = True
    p3.daemon = True

    # start that process
    p1.start()
    p2.start()
    p3.start()

    # The join() call ensures that subsequent lines of your code are not called before all the multiprocessing processes are completed. 
    # https://stackoverflow.com/a/25391661/11684146 & https://stackoverflow.com/a/60967514/11684146
    # p1.join()
    # p2.join()
    # p3.join()

    # Ensure that all processes are running
    # Kill all processes even if one process dies
    while True:
        time.sleep(0.5)
        if not all_processes_alive([p1, p2, p3]):
            time.sleep(0.05) # to prevent the main control from running ahead while processes terminate
            print("Student is using unfair practices, locking computer now")
            kill_all_processes([p1, p2, p3])
            time.sleep(0.5) # to prevent the main control from running ahead while processes terminate
            pc_locker.lock_pc()
            sys.exit()