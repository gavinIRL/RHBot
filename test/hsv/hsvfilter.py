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
    if object_name == "enemy_nametag":
        return HsvFilter(49, 0, 139, 91, 30, 197, 0, 0, 40, 38)
    if object_name == "message_boss_encounter":
        return HsvFilter(0, 92, 128, 13, 255, 255, 0, 0, 0, 0)
    if object_name == "display_boss_name_and_healthbar":
        return HsvFilter(0, 92, 123, 29, 255, 255, 0, 0, 0, 20)
    if object_name == "loot_chest_normal":
        # This is a difficult one to separate
        return HsvFilter(0, 34, 38, 28, 152, 124, 0, 0, 5, 12)
    if object_name == "map_outline":
        return HsvFilter(0, 85, 108, 12, 178, 205, 0, 13, 37, 50)
    if object_name == "gate_map_pos":
        # This is a very difficult one to separate
        return HsvFilter(15, 45, 38, 18, 200, 135, 0, 119, 0, 0)
    if object_name == "prompt_move_reward_screen":
        return HsvFilter(72, 98, 92, 105, 255, 225, 0, 54, 24, 38)
    if object_name == "prompt_select_card":
        return HsvFilter(79, 149, 140, 255, 255, 255, 0, 0, 0, 0)
    if object_name == "event_chest_special_appear":
        return HsvFilter(0, 124, 62, 88, 217, 246, 0, 0, 0, 0)
    if object_name == "inventory_green_item":
        return HsvFilter(37, 147, 0, 61, 255, 255, 0, 0, 0, 0)
    if object_name == "inventory_blue_item":
        return HsvFilter(79, 169, 0, 109, 246, 188, 0, 0, 0, 0)
    if object_name == "inventory_yellow_item":
        # This is a dangerous one as it can barely
        # distinguish against green items and vice versa
        return HsvFilter(19, 91, 107, 31, 168, 181, 0, 11, 32, 21)
    if object_name == "inventory_purple_item":
        return HsvFilter(126, 153, 0, 255, 255, 255, 0, 0, 0, 0)
    if object_name == "store_buttons":
        return HsvFilter(0, 0, 89, 43, 58, 240, 7, 1, 0, 0)
    if object_name == "":
        return HsvFilter()
    if object_name == "":
        return HsvFilter()
    if object_name == "":
        return HsvFilter()
    if object_name == "":
        return HsvFilter()
