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
from windowcapture import WindowCapture

pyautogui.FAILSAFE = True


class TestController():
    def __init__(self, loot=True, combat=True, freemove=False, rec_pb_only=False) -> None:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
        self.recording_ready = False
        self.recording_ongoing = False
        self.recorder = Recorder(self)
        self.playback = Playback(self)
        # This variable is for ignoring any move/combat bot loops
        self.rec_pb_only = rec_pb_only

        with open("gamename.txt") as f:
            gamename = f.readline()
        self.game_wincap = WindowCapture(gamename)

    def start_controller(self):
        self.start_countdown()
        self.start_mouse_listener()
        self.start_keypress_listener()
        while self.bot_running:
            # First check if any playback or record flags are on
            if self.perform_record_playback_checks():
                pass
            # Otherwise if this is rec/pb only then skip the usual logic
            elif self.rec_pb_only:
                time.sleep(0.5)
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
        elif self.recording_ready:
            # Start recording
            time.sleep(3)
            print("Now recording!")
            self.recording_ongoing = True
            self.recording_ready = False
            self.recorder.start_time = time.time()
            return True
        elif self.recording_ongoing:
            # This is to allow recording to go on
            time.sleep(0.5)
            return True

    def start_mouse_listener(self):
        self.mouse_listener = mouse.Listener(
            on_click=self.on_click)
        self.mouse_listener.start()
        self.mouse_listener.wait()  # Need to test if this is required

    def start_keypress_listener(self):
        if self.listener == None:
            self.listener = Listener(on_press=self.on_press,
                                     on_release=self.on_release)
            self.listener.start()

    def on_press(self, key):
        if self.recording_ongoing:
            # Log the event if not the end key
            if key == KeyCode(char='='):
                self.recording_ongoing = False
                self.recorder.write_recording_to_file()
                print("Finished recording #{}".format(
                    self.recorder.dest_file_count))
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
            # This is causing a bug if press escape
            if key == KeyCode(char='t'):
                self.playback_input_flag = not self.playback_input_flag
                print("Starting playback of #"+self.playback_string)
                self.playback_ongoing = True
            else:
                try:
                    self.playback_string += str(key.char)
                except:
                    pass

        elif key == KeyCode(char='t'):
            # This can only be reached if not entering playback number
            self.playback_input_flag = not self.playback_input_flag
            self.playback_string = ""
            print("Select a recording number")

        elif key == KeyCode(char='y'):
            print("Starting recording in 3 seconds")
            self.recording_ready = True

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
        if self.recording_ongoing:
            if key == KeyCode(char='-'):
                # Wipe all the collected data
                self.recording_ongoing = False
                self.recorder.unreleased_keys = []
                self.recorder.input_events = []
            else:
                try:
                    self.recorder.unreleased_keys.remove(key)
                except ValueError:
                    print('ERROR: {} not in unreleased_keys'.format(key))
                try:
                    self.recorder.record_event(
                        EventType.KEYUP, self.recorder.elapsed_time(), key.char)
                except AttributeError:
                    self.recorder.record_event(
                        EventType.KEYUP, self.recorder.elapsed_time(), key)

        if self.playback_ongoing:
            if key == KeyCode(char='-'):
                # find a way to stop the action playback
                self.playback_ongoing = False
                # Now need to release all keys while waiting for the
                # playback to catch up
                self.remove_all_keypresses()

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
                xratio, yratio = self.convert_click_to_ratio(x, y)
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

    def remove_all_keypresses(self):
        for key in ["up", "down", "left", "right"]:
            pyautogui.keyUp(key)
        for key in ["a", "s", "d", "f", "g", "h"]:
            pyautogui.keyUp(key)

    def convert_click_to_ratio(self, truex, truey):
        # This will grab the current rectangle coords of game window
        # and then turn the click values into a ratio of positions
        # versus the game window
        self.game_wincap.update_window_position(border=False)
        # Turn the screen pos into window pos
        relx = truex - self.game_wincap.window_rect[0] * 1.5
        rely = truey - self.game_wincap.window_rect[1] * 1.5
        # print("relx={}, rely={}".format(relx, rely))
        # print("winx={}, winy={}".format(
        #     self.game_wincap.window_rect[0], self.game_wincap.window_rect[1]))
        # print("winwidth={}".format(self.game_wincap.w))
        # Then convert to a ratio
        ratx = relx/(self.game_wincap.w*1.5)
        raty = rely/(self.game_wincap.h*1.5)
        return ratx, raty

    def convert_ratio_to_click(self, ratx, raty):
        # This will grab the current rectangle coords of game window
        # and then turn the ratio of positions versus the game window
        # into true x,y coords
        self.game_wincap.update_window_position(border=False)
        # Turn the ratios into relative
        relx = int(ratx * self.game_wincap.w)
        rely = int(raty * self.game_wincap.h)
        # Turn the relative into true
        truex = int(relx + self.game_wincap.window_rect[0] * 1.5)
        truey = int(rely + self.game_wincap.window_rect[1] * 1.5)
        return truex, truey

    def convert_pynput_to_pag(self, button):
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
        self.dest_file_count = 0

    def elapsed_time(self):
        return time.time() - self.start_time

    def write_recording_to_file(self):
        # Here will write to the json file
        # write the output to a file
        script_dir = os.path.dirname(__file__)
        dest_dir = os.path.join(
            script_dir,
            'recordings')
        # Now get the number of files in recordings folder already
        _, _, files = next(os.walk(dest_dir))
        self.dest_file_count = len(files) + 1
        dest_file_name = str(self.dest_file_count)
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

    def move_mouse_centre(self):
        pyautogui.moveTo(900, 500, 0.05)

    def playActions(self, filename):
        # The usual logic here
        # Only difference is that first thing need to do is sleep for 3 seconds
        print("Starting playback in 2 seconds")
        time.sleep(2)
        print("Starting playback")
        # and then will move the mouse to stop any flow/mwb problems
        self.move_mouse_centre()
        # And then continue
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
                action_start_time = time.time()

                # Need to exit if the terminate key is pressed
                if not self.controller.playback_ongoing:
                    break

                # look for escape input to exit
                # if action['button'] == 'Key.esc':
                #     break

                # perform the action
                if action['type'] == 'keyDown':
                    key = self.controller.convert_pynput_to_pag(
                        action['button'])
                    pyautogui.keyDown(key)
                    # print("keyDown on {}".format(key))
                elif action['type'] == 'keyUp':
                    key = self.controller.convert_pynput_to_pag(
                        action['button'])
                    pyautogui.keyUp(key)
                    # print("keyUp on {}".format(key))

                elif action['type'] == 'click':
                    # To-do: need to convert ratio into actual positions
                    print("ratiox={}".format(action['pos'][0]), end='')
                    print("  ratioy={}".format(action['pos'][1]))

                    x, y = self.controller.convert_ratio_to_click(action['pos'][0],
                                                                  action['pos'][1])
                    print("truex={}".format(x), end='')
                    print("  truey={}".format(y))
                    pyautogui.click(x, y, duration=0.15)
                    # print("click on {}".format(action['pos']))

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
                elapsed_time -= (time.time() - action_start_time)
                if elapsed_time < 0:
                    elapsed_time = 0
                # print('sleeping for {}'.format(elapsed_time))
                time.sleep(elapsed_time)
        print("Finished playback")


if __name__ == "__main__":
    cont = TestController(freemove=True)
    cont.start_controller()
