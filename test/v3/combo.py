# This file will hold the weapon-specific information
# And will include the preferred combinations of attacks
# And hold the basic information of cooldown times, etc.

class WeaponBag():
    # The preferred layout of skills for this class is as follows:
    # a =
    # s =
    # d =
    # f =
    # g =
    def __init__(self, level, focused) -> None:
        self.level = level
        self.focused = focused

    def grab_base_cooldowns(self):
        cooldowns = {"a": 5}
        cooldowns["s"] = 5
        cooldowns["d"] = 5
        cooldowns["f"] = 5
        cooldowns["g"] = 5
        cooldowns["h"] = 5

        cooldowns["s+a"] = 5
        cooldowns["s+s"] = 5
        cooldowns["s+d"] = 5
        cooldowns["s+f"] = 5
        cooldowns["s+g"] = 5
        cooldowns["s+h"] = 5

        cooldowns["f1"] = 5
        cooldowns["f2"] = 5
        cooldowns["f3"] = 5
        cooldowns["f4"] = 5
        # Need to adjust based on level and if focused or not
        return cooldowns

    def grab_preferred_combo(current_cds):
        # For a given set of conditions this will choose
        # the preferred attack combination
        pass

    def grab_zoneprep(current_cds):
        # This will
        pass
