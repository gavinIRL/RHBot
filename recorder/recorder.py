# This will be the script used to record all actions to help with bot creation
from pynput import mouse, keyboard
from time import time
import os


class Recorder():
    def __init__(self) -> None:
        self.unreleased_keys = None

    def main(self):
        self.run_listeners()

    def run_listeners(self):

        # Collect mouse input events
        global mouse_listener
        mouse_listener = mouse.Listener(on_click=self.on_click)
        mouse_listener.start()
        mouse_listener.wait()  # wait for the listener to become ready

        # Collect keyboard inputs until released
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            global start_time
            start_time = time()
            listener.join()

    def on_press(self, key):
        # we only want to record the first keypress event until that key has been released

        if key in self.unreleased_keys:
            return
        else:
            self.append(key)
        print("Key Pressed")

    def on_release(self, key):
        # mark key as no longer pressed
        try:
            self.unreleased_keys.remove(key)
        except ValueError:
            print('ERROR: {} not in unreleased_keys'.format(key))

    def on_click(self, x, y, button, pressed):
        # when pressed is False, that means it's a release event.
        # let's listen only to mouse click releases
        if not pressed:
            print("Clicked")


if __name__ == "__main__":
    rc = Recorder()
    rc.main()
