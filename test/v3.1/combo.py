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

    def __init__(self, level=1) -> None:
        self.level = level

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

    def grab_preferred_combo(self):
        # For a given set of conditions this will choose
        # the preferred attack combination
        returnlist = [["x", 0.07]]
        returnlist.append(["point", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["point", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["x", 0.07])
        returnlist.append(["point", 0.07])
        returnlist.append(["c", 0.25])

        return returnlist

    def grab_zoneprep(self):
        # This will
        pass


class WeaponBagUnfocused():
    # The preferred layout of skills for this class is as follows:
    # s = spiked mat
    # d = charge shot
    # f = lock on
    # g = shockmine
    # h = sentry laser

    def __init__(self, level=1) -> None:
        self.level = level

    def grab_base_cooldowns(self):
        cooldowns = {"a": False}
        cooldowns["s"] = 5.3
        cooldowns["d"] = 4.4
        cooldowns["f"] = 8.8
        cooldowns["g"] = 17
        cooldowns["h"] = 41

        cooldowns["s+a"] = False
        cooldowns["s+s"] = False
        cooldowns["s+d"] = False
        cooldowns["s+f"] = False
        cooldowns["s+g"] = False
        cooldowns["s+h"] = False

        cooldowns["f1"] = False
        cooldowns["f2"] = False
        cooldowns["f3"] = False
        cooldowns["f4"] = False
        # Need to adjust based on level and if focused or not
        return cooldowns

    def grab_preferred_combo(self):
        # For a given set of conditions this will choose
        # the preferred attack combination
        returnlist = []
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["point", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["x", 0.2])
        returnlist.append(["point", 0.2])
        return returnlist

    def grab_zoneprep(self):
        # This will
        pass


class MSUnfocused():
    # The preferred layout of skills for this class is as follows:
    # a = magic missile
    # s =
    # d =
    # f = windy blast
    # g =
    # h = sandstorm

    def __init__(self, level=1) -> None:
        self.level = level

    def grab_base_cooldowns(self):
        cooldowns = {"a": 5.3}
        cooldowns["s"] = False
        cooldowns["d"] = False
        if self.level >= 2:
            cooldowns["f"] = 5.5
        else:
            cooldowns["h"] = False
        cooldowns["g"] = False
        if self.level >= 2:
            cooldowns["h"] = 8.9
        else:
            cooldowns["h"] = False

        cooldowns["s+a"] = False
        cooldowns["s+s"] = False
        cooldowns["s+d"] = False
        cooldowns["s+f"] = False
        cooldowns["s+g"] = False
        cooldowns["s+h"] = False

        cooldowns["f1"] = False
        cooldowns["f2"] = False
        cooldowns["f3"] = False
        cooldowns["f4"] = False
        # Need to adjust based on level and if focused or not
        return cooldowns

    def grab_preferred_order(self):
        return ("a", "f", "h")

    def grab_preferred_combo(self):
        # For a given set of conditions this will choose
        # the preferred attack combination
        returnlist = []
        returnlist.append(["a", 0.2])
        returnlist.append(["point", 0.2])
        returnlist.append(["f", 0.2])
        returnlist.append(["h", 0.2])
        # But need to make sure they have been unlocked first
        checklist = self.grab_base_cooldowns()
        truelist = []
        for key, dur in returnlist:
            if key in checklist:
                truelist.append([key, dur])
            elif key == "point":
                truelist.append([key, dur])
            elif key == "x":
                truelist.append([key, dur])
            elif key == "move":
                truelist.append([key, dur])
            elif key == "move_player":
                truelist.append([key, dur])
        return truelist

    def grab_zoneprep(self):
        # This will
        pass


class MSFocused():
    # The preferred layout of skills for this class is as follows:
    # a = magic missile
    # s =
    # d = soul eroder
    # f = windy blast
    # g = phantom missile
    # h = sandstorm
    # s+a = pillar of light
    # s+s = blinding beam

    def __init__(self, level=1) -> None:
        self.level = level

    def grab_base_cooldowns(self):
        cooldowns = {"a": 4.4}
        cooldowns["s"] = False
        cooldowns["d"] = 2.1
        cooldowns["f"] = 5.5
        cooldowns["g"] = 4.4
        cooldowns["h"] = 8.9

        cooldowns["s+a"] = 32
        if self.level >= 30:
            cooldowns["s+s"] = 41
        else:
            cooldowns["s+s"] = False
        cooldowns["s+d"] = False
        cooldowns["s+f"] = False
        cooldowns["s+g"] = False
        cooldowns["s+h"] = False

        cooldowns["f1"] = False
        cooldowns["f2"] = False
        cooldowns["f3"] = False
        cooldowns["f4"] = False
        # Need to adjust based on level and if focused or not
        return cooldowns

    def grab_preferred_order(self):
        return ("a", "g", "h", "f", "s+s", "d")

    def grab_preferred_combo(self):
        # For a given set of conditions this will choose
        # the preferred attack combination
        returnlist = []
        returnlist.append(["a", 0.2])
        returnlist.append(["g", 0.2])
        returnlist.append(["h", 0.2])
        returnlist.append(["point", 0.2])
        returnlist.append(["f", 0.2])
        return returnlist

    def grab_zoneprep(self):
        # This will
        pass
