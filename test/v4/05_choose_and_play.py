# This file will allow the user to quickly choose
# an action-sequence to play and then carry out the action sequence
# It will wait in the background until a certain key is pressed
# and then it will perform another action
from pynput.keyboard import Key, Listener, KeyCode
from pynput import mouse
import time
import os
import pydirectinput as pyautogui
import json

pyautogui.FAILSAFE = True


class TestController():
    def __init__(self, loot=True, combat=True, freemove=False) -> None:
        self.mode = "movement"
        self.listener = None
        self.mouse_listener = None
        self.bot_running = False
        self.loot_enabled = loot
        self.combat_enabled = combat
        self.freemove_enabled = freemove
        self.playback_input_flag = False
        self.playback_ongoing = False
        self.playback_string = ""
        self.recording_ongoing = False
        self.recorder = Recorder(self)
        self.playback = Playback(self)

    def start_controller(self):
        self.start_countdown()
        self.start_mouse_listener()
        self.start_keypress_listener()
        while self.bot_running:
            # First check if any playback or record flags are on
            if self.perform_record_playback_checks():
                pass
            # Then continue with the usual loop
            # Shouldn't need to stop everything
            # As shouldn't be in a dungeon when doing this
            else:
                # Perform the usual loop stuff here
                # Will also need to add logic to the combat and move
                # main loops to break if any of the rec/playback checks
                # return true
                time.sleep(0.5)

    def perform_record_playback_checks(self):
        if self.playback_ongoing:
            # This is when the playback gets called
            self.playback.playActions(self.playback_string+".json")
            time.sleep(0.5)
            self.playback_ongoing = False
            return True
        elif self.playback_input_flag:
            # This is for when inputting the details
            time.sleep(0.5)
            return True
        elif self.recording_ongoing:
            # In this case will start a recording
            time.sleep(0.5)
            return True

    def start_mouse_listener(self):
        self.mouse_listener = mouse.Listener(
            on_click=self.on_click, suppress=True)
        self.mouse_listener.start()
        self.mouse_listener.wait()  # Need to test if this is required

    def start_keypress_listener(self):
        if self.listener == None:
            self.listener = Listener(on_press=self.on_press,
                                     on_release=self.on_release, suppress=True)
            self.listener.start()

    def on_press(self, key):
        if self.recording_ongoing:
            # Log the event if not the end key
            if key == KeyCode(char='='):
                self.recording_ongoing = False
                self.recorder.write_recording_to_file()
            else:
                if key not in self.recorder.unreleased_keys:
                    self.recorder.unreleased_keys.append(key)
                    try:
                        self.recorder.record_event(
                            EventType.KEYDOWN, self.recorder.elapsed_time(), key.char)
                    except AttributeError:
                        self.recorder.record_event(
                            EventType.KEYDOWN, self.recorder.elapsed_time(), key)

        elif self.playback_ongoing:
            # Do nothing
            pass

        elif self.playback_input_flag:
            # add the key to existing string
            self.playback_string += str(key.char)

        elif key == KeyCode(char='t'):
            self.playback_input_flag = not self.playback_input_flag
            if self.playback_input_flag:
                self.playback_string = ""
                print("Select a recording number")
            else:
                # To-do: Start the playback
                print("Starting playback of #"+self.playback_string)
                self.playback_ongoing = True

        elif key == KeyCode(char='y'):
            self.recording_ongoing = True
            self.recorder.start_time = time.time()
            print("Starting recording in 3 seconds")

        elif key == KeyCode(char='w'):
            self.loot_enabled = not self.loot_enabled
            if self.loot_enabled:
                print("LOOT ON")
            else:
                print("LOOT OFF")

        elif key == KeyCode(char='e'):
            self.combat_enabled = not self.combat_enabled
            if self.combat_enabled:
                print("COMBAT ON")
            else:
                print("COMBAT OFF")

        elif key == KeyCode(char='r'):
            self.freemove_enabled = not self.freemove_enabled
            if self.freemove_enabled:
                print("FREEMOVE ON")
            else:
                print("FREEMOVE OFF")

    def on_release(self, key):
        # Need to have an exit recording or playback only button (=?)
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
        if self.recording_ongoing:
            if not pressed:
                # Need to get the ratio compared to window top left
                # This will allow common usage on other size monitors
                xratio, yratio = self.convert_click_to_relative(x, y)
                self.recorder.record_event(
                    EventType.CLICK, self.recorder.elapsed_time(), button, (xratio, yratio))

    def start_countdown(self):
        print("Bot starting in 3 seconds")
        time.sleep(1)
        print("Bot starting in 2 seconds")
        time.sleep(1)
        print("Bot starting in 1 seconds")
        time.sleep(1)
        self.bot_running = True

    def convert_click_to_relative(self, x, y):
        # This will grab the current rectangle coords of game window
        # and then turn the click values into a ratio of positions
        # versus the game window
        with open("gamename.txt") as f:
            gamename = f.readline()
        # Now grab the window rectangle

        return x, y

    def convert_relative_to_click(self, x, y):
        # This will grab the current rectangle coords of game window
        # and then turn the ratio of positions versus the game window
        # into true x,y coords
        with open("gamename.txt") as f:
            gamename = f.readline()
        # Now grab the window rectangle
        return x, y

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
    def __init__(self, controller: TestController) -> None:
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

    def write_recording_to_file(self):
        # Here will write to the json file
        # write the output to a file
        script_dir = os.path.dirname(__file__)
        dest_dir = os.path.join(
            script_dir,
            'recordings')
        # Now get the number of files in recordings folder already
        _, _, files = next(os.walk(dest_dir))
        dest_file_count = len(files) + 1
        dest_file_name = str(dest_file_count)
        filepath = os.path.join(
            dest_dir,
            '{}.json'.format(dest_file_name)
        )
        with open(filepath, 'w') as outfile:
            json.dump(self.input_events, outfile, indent=4)

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


class Playback():
    def __init__(self, controller: TestController) -> None:
        self.controller = controller

    def playActions(self, filename):
        # The usual logic here
        # Only difference is that first thing need to do is sleep for 3 seconds
        time.sleep(3)
        # and then will move the mouse to stop any flow/mwb problems
        script_dir = os.path.dirname(__file__)
        filepath = os.path.join(
            script_dir,
            'recordings',
            filename
        )
        with open(filepath, 'r') as jsonfile:
            # parse the json
            data = json.load(jsonfile)

            # loop over each action
            # Because we are not waiting any time before executing the first action, any delay before the initial
            # action is recorded will not be reflected in the playback.
            for index, action in enumerate(data):
                action_start_time = time()

                # look for escape input to exit
                if action['button'] == 'Key.esc':
                    break

                # perform the action
                if action['type'] == 'keyDown':
                    key = self.controller.convert_pynput_to_pag(
                        action['button'])
                    pyautogui.keyDown(key)
                    print("keyDown on {}".format(key))
                elif action['type'] == 'keyUp':
                    key = self.controller.convert_pynput_to_pag(
                        action['button'])
                    pyautogui.keyUp(key)
                    print("keyUp on {}".format(key))

                elif action['type'] == 'click':
                    # To-do: need to convert ratio into actual positions
                    x, y = self.controller.convert_relative_to_click(action['pos'][0],
                                                                     action['pos'][1])
                    pyautogui.click(x, y, duration=0.15)
                    print("click on {}".format(action['pos']))

                # then sleep until next action should occur
                try:
                    next_action = data[index + 1]
                except IndexError:
                    # this was the last action in the list
                    break
                elapsed_time = next_action['time'] - action['time']

                # if elapsed_time is negative, that means our actions are not ordered correctly. throw an error
                if elapsed_time < 0:
                    raise Exception('Unexpected action ordering.')

                # adjust elapsed_time to account for our code taking time to run
                elapsed_time -= (time() - action_start_time)
                if elapsed_time < 0:
                    elapsed_time = 0
                print('sleeping for {}'.format(elapsed_time))
                time.sleep(elapsed_time)


if __name__ == "__main__":
    cont = TestController(freemove=True)
    cont.start_controller()
