# This file will hold the weapon-specific information
# And will include the preferred combinations of attacks
# And hold the basic information of cooldown times, etc.

class WeaponBagFocused():
    # The preferred layout of skills for this class is as follows:
    # a = overhand
    # s = backhand
    # d = cannon spike
    # f = lock on
    # g = jet bike
    # h = summon mk-2
    # s+a = electric line
    # s+s = shockmine
    # s+d = sentry laser
    # s+f = spiked mat
    # f1 = stun grenade
    # f2 = concentration

    def __init__(self, level, focused) -> None:
        self.level = level
        self.focused = focused

    def grab_base_cooldowns(self):
        cooldowns = {"a": 5.5}
        cooldowns["s"] = 5.3
        cooldowns["d"] = 4.4
        cooldowns["f"] = 8.8
        cooldowns["g"] = 17
        cooldowns["h"] = 41

        cooldowns["s+a"] = 10.2
        cooldowns["s+s"] = 7.8
        cooldowns["s+d"] = 17.6
        cooldowns["s+f"] = 30
        cooldowns["s+g"] = False
        cooldowns["s+h"] = False

        cooldowns["f1"] = 85
        cooldowns["f2"] = 300
        cooldowns["f3"] = False
        cooldowns["f4"] = False
        # Need to adjust based on level and if focused or not
        return cooldowns

    def grab_preferred_combo(current_cds):
        # For a given set of conditions this will choose
        # the preferred attack combination
        pass

    def grab_zoneprep(current_cds):
        # This will
        pass
