# This will be the file which handles the combat mode
# The keypresses themselves will be drawn from the combo file
# In particular the relevant weapon in the combo file

class Combat():
    def __init__(self, enabled, weapon="WB") -> None:
        # Variable to turn combat on/off from main loop
        self.enabled = enabled
        # Variable to determine which combos to use
        self.weapon = weapon

        # Variables for keeping track of which skills are on cooldown
        # Basic asdfgh skills up first
        self.cd_a = 0
        self.cd_s = 0
        self.cd_d = 0
        self.cd_f = 0
        self.cd_g = 0
        self.cd_h = 0
        # Then the shift + asdfgh skills
        self.cd_sa = 0
        self.cd_ss = 0
        self.cd_sd = 0
        self.cd_sf = 0
        self.cd_sg = 0
        self.cd_sh = 0
        # Then the buff skills
        self.cd_f1 = 0
        self.cd_f2 = 0
        self.cd_f3 = 0
        self.cd_f4 = 0

    def update_cooldowns(self):
        pass

    def start(self):
        pass

    def run(self):
        pass

    def stop(self):
        pass

    def update_target(self):
        # This is for pointing character in correct direction
        # Want to always be pointed towards the bulk of the enemies
        pass
