import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class text_transfer:
    def __init__(self):
        # 之前专门写个type transfer好像没啥用，直接两个列表对一下index拉倒了。
        self.__init_type()

    def __init_type(self):
        # 这个就是把那些ID的类型弄过来整成一个列表以备后用。
        # 红方坦克：MainBattleTank_ZTZ100，蓝方坦克：MainBattleTank_ZTZ200，红方步兵战车：WheeledCmobatTruck_ZB100，蓝方步兵战车：WheeledCmobatTruck_ZB200，步兵班：infantry，自行迫榴炮：Howitzer_C100，无人突击车：ArmoredTruck_ZTL100，无人机：ShipboardCombat_plane，导弹发射车：missile_truck。
        self.type_list = ["MainBattleTank_ZTZ100","MainBattleTank_ZTZ200","WheeledCmobatTruck_ZB100","WheeledCmobatTruck_ZB200","infantry","Howitzer_C100","ArmoredTruck_ZTL100","ShipboardCombat_plane","missile_truck"]
        self.type_list_CN = ["坦克","坦克","步兵战车","步兵战车","步兵班","自行迫榴炮","无人突击车","无人机","导弹发射车"]
    
    def status_to_text(self,status_json):
        # 这个把读出来的JSON文件转换成一段叙述。
        unit_all = status_json["UnitState"]
        unit_all_list = list(unit_all.keys())
        result_text = ""
        for unit_type in self.type_list:
            count_red = 0 
            count_blue = 0 
            for unit_id_single in unit_all_list:
                if unit_type in unit_id_single:
                    if unit_all[unit_id_single]["PlayerName"] == "redPlayer":
                        count_red += 1
                    else:
                        count_blue += 1
                #然后生成一段话
                if count_red != 0:
                    result_text += "红方" + self.type_list_CN[self.type_list.index(unit_type)] + "有" + str(count_red) + "个。\n"
                if count_blue != 0:
                    result_text += "蓝方" + self.type_list_CN[self.type_list.index(unit_type)] + "有" + str(count_blue) + "个。\n"
        return result_text
            
        pass 
if __name__ == '__main__':
    from json_editor.json_editor import json_editor
    shishi_json = json_editor()
    shishi_json.set_location(r"C:\Users\42418\Desktop\2024ldjs\EnglishMulu\test_scene\auto_test\new1.Json")
    shishi_json.load_json()
    shishi = text_transfer()
    jieguo = shishi.status_to_text(shishi_json.json_data)

