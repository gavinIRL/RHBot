# This file will allow the user to quickly choose
# an action-sequence to play and then carry out the action sequence
# It will wait in the background until a certain key is pressed
# and then it will perform another action
from pynput.keyboard import Key, Listener, KeyCode
import time
import os


class TestController():
    def __init__(self, loot=True, combat=True, freemove=False) -> None:
        self.mode = "movement"
        self.listener = None
        self.bot_running = False
        self.loot_enabled = loot
        self.combat_enabled = combat
        self.freemove_enabled = freemove
        self.playback_input_flag = False
        self.playback_ready = False
        self.playback_string = ""
        self.recording_ready = False
        self.recorder = Recorder()

    def start_controller(self):
        self.start_countdown()
        self.start_keypress_listener()
        while self.bot_running:
            # First check if any playback or record flags are on
            self.perform_record_playback_checks()
            # Then continue with the usual loop
            # Shouldn't need to stop everything
            # As shouldn't be in a dungeon when doing this
            time.sleep(0.5)

    def perform_record_playback_checks(self):
        if self.playback_ready:
            # This is when the playback gets called
            self.playActions(self.playback_string+".json")
            time.sleep(0.5)
            self.playback_ready = False
        elif self.playback_input_flag:
            # This is for when inputting the details
            time.sleep(0.5)
        elif self.recording_ready:
            # In this case will start a recording
            pass

    def start_keypress_listener(self):
        if self.listener == None:
            self.listener = Listener(on_press=self.on_press,
                                     on_release=self.on_release, suppress=True)
            self.listener.start()

    def on_press(self, key):
        if key == KeyCode(char='t'):
            self.playback_input_flag = not self.playback_input_flag
            if self.playback_input_flag:
                self.playback_string = ""
                print("Select a recording number")
            else:
                # To-do: Start the playback
                print("Starting recording number "+self.playback_string)
                self.playback_ready = True
        elif self.playback_input_flag:
            # add the key to existing string
            self.playback_string += str(key.char)
        else:
            if key == KeyCode(char='w'):
                self.loot_enabled = not self.loot_enabled
                if self.loot_enabled:
                    print("LOOT ON")
                else:
                    print("LOOT OFF")
            if key == KeyCode(char='e'):
                self.combat_enabled = not self.combat_enabled
                if self.combat_enabled:
                    print("COMBAT ON")
                else:
                    print("COMBAT OFF")
            if key == KeyCode(char='r'):
                self.freemove_enabled = not self.freemove_enabled
                if self.freemove_enabled:
                    print("FREEMOVE ON")
                else:
                    print("FREEMOVE OFF")

    def on_release(self, key):
        if key == KeyCode(char='q'):
            self.bot_running = False
            # self.combatbat.running = False
            # Need to pause for 1 second and then clear all keypresses
            time.sleep(0.5)
            # self.combatbat.remove_all_keypresses()
            print("Exiting bot")
            os._exit(1)

    def on_click(self, x, y, button, pressed):
        # when pressed is False, that means it's a release event.
        # let's listen only to mouse click releases
        if self.recording_ready:
            if not pressed:
                self.recorder.record_event(
                    EventType.CLICK, self.recorder.elapsed_time(), button, (x, y))

    def start_countdown(self):
        print("Bot starting in 3 seconds")
        time.sleep(1)
        print("Bot starting in 2 seconds")
        time.sleep(1)
        print("Bot starting in 1 seconds")
        time.sleep(1)
        self.bot_running = True

    def playActions(self, filename):
        # The usual logic here, not going to include it here
        # Only difference is that first thing need to do is sleep for 3 seconds

        pass

    def convert_pynput_to_pag(button):
        PYNPUT_SPECIAL_CASE_MAP = {
            'alt_l': 'altleft',
            'alt_r': 'altright',
            'alt_gr': 'altright',
            'caps_lock': 'capslock',
            'ctrl_l': 'ctrlleft',
            'ctrl_r': 'ctrlright',
            'page_down': 'pagedown',
            'page_up': 'pageup',
            'shift_l': 'shiftleft',
            'shift_r': 'shiftright',
            'num_lock': 'numlock',
            'print_screen': 'printscreen',
            'scroll_lock': 'scrolllock',
        }

        # example: 'Key.F9' should return 'F9', 'w' should return as 'w'
        cleaned_key = button.replace('Key.', '')

        if cleaned_key in PYNPUT_SPECIAL_CASE_MAP:
            return PYNPUT_SPECIAL_CASE_MAP[cleaned_key]

        return cleaned_key


class EventType():
    KEYDOWN = 'keyDown'
    KEYUP = 'keyUp'
    CLICK = 'click'


class Recorder():
    def __init__(self, controller) -> None:
        self.controller = controller
        # declare mouse_listener globally so that keyboard on_release can stop it
        self.mouse_listener = controller.listener
        # declare our start_time globally so that the callback functions can reference it
        self.start_time = None
        # keep track of unreleased keys to prevent over-reporting press events
        self.unreleased_keys = []
        # storing all input events
        self.input_events = []

    def elapsed_time(self):
        return time() - self.start_time

    def start_recording(self):
        # This will be the main recording logic flow
        # Maybe will need to do this in controller?
        pass

    def record_event(self, event_type, event_time, button, pos=None):
        self.input_events.append({
            'time': event_time,
            'type': event_type,
            'button': str(button),
            'pos': pos
        })

        if event_type == EventType.CLICK:
            pass
            # print('{} on {} pos {} at {}'.format(
            #     event_type, button, pos, event_time))
        else:
            pass
            # print('{} on {} at {}'.format(event_type, button, event_time))


if __name__ == "__main__":
    cont = TestController(freemove=True)
    cont.start_controller()
