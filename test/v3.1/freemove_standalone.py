# This file will allow the user to freely move the character
# But once an enemy is detected it will swap to combat mode

class StandaloneFreeMove():
    def __init__(self, controller) -> None:
        self.controller = controller

    def freemove_mainloop(self):
        print("Returning control to player")
        exit_reason = None
        while self.controller.freemove_enabled:
            break
        if exit_reason != "combat":
            print("Returning to automatic navigation")
