from win32gui import GetWindowText, GetForegroundWindow
import sys

def get_current_window():
    return(GetWindowText(GetForegroundWindow()))

def partial_match_exists(list_of_strings, x): # https://stackoverflow.com/a/64127141/11684146
    for string in list_of_strings:
        if string in x:
            return True
    return False

def check_illegal_window(exactly_allowed_titles=[], partially_allowed_titles=[]):
    """
    exactly_allowed_window_titles = list of strings 
        eg: exactly_allowed_titles = ['VS Code']
            - 'VS Code - main.py' -> not allowed

    partially_allowed_titles = list of strings
        eg: partially_allowed_titles = ['VS Code']
            - 'VS Code - main.py' -> allowed
    """

    while True:
        window_title = get_current_window()

        if window_title in ['Task Switching', '']:
            continue
        
        # check partially allowed titles
        if partially_allowed_titles: # check if list is empty/full - pythonic way | https://stackoverflow.com/a/53522/11684146
            if not partial_match_exists(partially_allowed_titles, window_title):
                print("exiting1")
                sys.exit()

        # check exactly allowed titles
        if exactly_allowed_titles:
            if window_title not in exactly_allowed_titles:
                print("exiting2")
                sys.exit()
    

check_illegal_window(partially_allowed_titles=['Code', 'Brave']) # working 
# check_illegal_window(exactly_allowed_titles=['window_monitor.py - Final Year Project - Visual Studio Code']) # working
# print(get_current_window()) # working 