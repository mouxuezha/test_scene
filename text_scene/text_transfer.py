import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class text_transfer:
    def __init__(self):
        # 之前专门写个type transfer好像没啥用，直接两个列表对一下index拉倒了。
        self.__init_type()
        self.num_commands = [0,0] # 第一个是转化成功的commands，第二个是转化失败的commands 


    def __init_type(self):
        # 这个就是把那些ID的类型弄过来整成一个列表以备后用。
        # 红方坦克：MainBattleTank_ZTZ100，蓝方坦克：MainBattleTank_ZTZ200，红方步兵战车：WheeledCmobatTruck_ZB100，蓝方步兵战车：WheeledCmobatTruck_ZB200，步兵班：Infantry，自行迫榴炮：Howitzer_C100，无人突击车：ArmoredTruck_ZTL100，无人机：ShipboardCombat_plane，导弹发射车：missile_truck。
        self.type_list = ["MainBattleTank_ZTZ100","MainBattleTank_ZTZ200","WheeledCmobatTruck_ZB100","WheeledCmobatTruck_ZB200","Infantry","Howitzer_C100","ArmoredTruck_ZTL100","ShipboardCombat_plane","missile_truck"]
        self.type_list_CN = ["坦克","坦克","步兵战车","步兵战车","步兵班","自行迫榴炮","无人突击车","无人机","导弹发射车"]
        self.command_type_list = ["add","delete"]
    
    def status_to_text(self,status_json):
        # 这个把读出来的JSON文件转换成一段叙述。
        unit_all = status_json["UnitState"]
        unit_all_list = list(unit_all.keys())
        result_text_red = "红方："
        result_text_blue = "蓝方："
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
                result_text_red += self.type_list_CN[self.type_list.index(unit_type)] + "有" + str(count_red) + "个。"
            if count_blue != 0:
                result_text_blue += self.type_list_CN[self.type_list.index(unit_type)] + "有" + str(count_blue) + "个。"
            result_text = result_text_red + result_text_blue
        return result_text
            
    def text_to_commands(self, text:str):
        # 这个是从一段话里面把命令提取出来
        commands = []
        for command_type in self.command_type_list:
            if command_type == "add":
                index_list = self.find_all_str(text, command_type) 
                for i in range(len(index_list)):
                    sub_str = text[index_list[i]:-1]
                    try:
                        unit_type = self.cut_from_str(sub_str, "unit_type=", ",")
                        team_id = self.cut_from_str(sub_str, "team_id=", "]")
                        command_single = {"type": command_type, "unit_type": unit_type, "team_id": team_id}
                        commands.append(command_single)
                        self.num_commands[0] += 1
                    except:
                        self.num_commands[1] += 1
                        print("G in one add command")
            if command_type == "delete":
                index_list = self.find_all_str(text, command_type)
                for i in range(len(index_list)):
                    sub_str = text[index_list[i]:-1]
                    try:
                        unit_type = self.cut_from_str(sub_str, "unit_type=", ",")
                        team_id = self.cut_from_str(sub_str, "team_id=", "]")
                        command_single = {"type": command_type, "unit_type": unit_type, "team_id": team_id}
                        commands.append(command_single)
                        self.num_commands[0] += 1
                    except:
                        self.num_commands[1] += 1
                        print("G in one delete command")
        return commands


    def find_all_str(self, text:str, sub_str:str):
        index_list = [] 
        index = text.find(sub_str)
        while index != -1:
            index_list.append(index)
            index = text.find(sub_str, index + 1)
        
        return index_list
    
    def cut_from_str(self, text:str, str_qian:str, str_hou:str):
        # 需要把数字从字符串中抠出来.不是数字也不影响
        # 先找到数字的起始位置.
        index_qian = text.find(str_qian)
        sub_str = text[index_qian+len(str_qian):]
        index_hou = sub_str.find(str_hou)
        # index_hou = text.find(str_hou)
        number_str = sub_str[0:index_hou]
        # number_float = float(number_str)
        return number_str    
if __name__ == '__main__':
    flag = 1
    if flag == 0:
        from json_editor.json_editor import json_editor
        shishi_json = json_editor()
        shishi_json.set_location(r"C:\Users\42418\Desktop\2024ldjs\EnglishMulu\test_scene\auto_test\new1.Json")
        shishi_json.load_json()
        shishi = text_transfer()
        jieguo = shishi.status_to_text(shishi_json.json_data)
    elif flag == 1:
        response_str = '好的，已将按照您的要求更新了场景。以下是更新后的场景编辑指令：\n\n[add, unit_type=MainBattleTank_ZTZ200, team_id=1],\n[add, unit_type=WheeledCmobatTruck_ZB100, team_id=0],\n[add, unit_type=infantry, team_id=0],\n[delete, unit_type=WheeledCmobatTruck_ZB200, team_id=0],\n[delete, unit_type=missile_truck, team_id=0],\n\n请注意，我已经将蓝方自行迫榴炮和导弹发射车从场景中删除了，并增加了红方的一个步兵战车和一个坦克。\n\n如果您还有其他需求，请随时告诉我。'
        shishi = text_transfer()
        jieguo = shishi.text_to_commands(response_str)
        print(jieguo)
    

