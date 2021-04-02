# custom data structure to hold the state of an HSV filter
class HsvFilter:
    def __init__(self, hMin=None, sMin=None, vMin=None, hMax=None, sMax=None, vMax=None,
                 sAdd=None, sSub=None, vAdd=None, vSub=None):
        self.hMin = hMin
        self.sMin = sMin
        self.vMin = vMin
        self.hMax = hMax
        self.sMax = sMax
        self.vMax = vMax
        self.sAdd = sAdd
        self.sSub = sSub
        self.vAdd = vAdd
        self.vSub = vSub


# Putting this here out of the way as it's a chonk
def grab_preset_filter(object_name=None) -> HsvFilter:
    if object_name is None:
        return HsvFilter(0, 0, 0, 255, 255, 255, 0, 0, 0, 0)
    if object_name == "enemy_map_loc":
        return HsvFilter(0, 128, 82, 8, 255, 255, 0, 66, 30, 34)
    if object_name == "player_map_loc":
        return HsvFilter(31, 94, 86, 73, 255, 255, 0, 0, 0, 0)
    if object_name == "other_player_map_loc":
        return HsvFilter(16, 172, 194, 26, 255, 255, 0, 0, 70, 37)
    if object_name == "loot_distant":
        return HsvFilter(14, 116, 33, 32, 210, 59, 16, 0, 3, 0)
    if object_name == "loot_near":
        return HsvFilter(0, 155, 135, 31, 240, 217, 0, 0, 0, 0)
    if object_name == "prompt_press_x_pickup":
        return HsvFilter(78, 110, 110, 97, 189, 255, 0, 0, 0, 0)
    if object_name == "message_section_cleared":
        return HsvFilter(0, 0, 214, 179, 65, 255, 0, 0, 0, 17)
    if object_name == "message_go":
        return HsvFilter(32, 114, 89, 58, 255, 255, 0, 12, 0, 0)
    if object_name == "":
        return HsvFilter()
    if object_name == "":
        return HsvFilter()
    if object_name == "":
        return HsvFilter()
