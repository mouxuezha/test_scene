# 这个是具体执行编辑的
import json
import queue
import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class json_editor():
    def __init__(self):
        self.json_location = r"auto_test\new1.jeson"
        self.commands_queue = queue.Queue(maxsize=114514) # 这个是新加的，用来处理和大模型的交互。
        self.num = 0 
        self.json_data = None
        self.json_data_original = None
        pass 
    
    def set_location(self,location):
        # 这个是外部设定需要编辑的东西的路径 
        self.json_location = location
        
    def load_json(self):
        # 这个是加载json文件
        with open(self.json_location, 'r', encoding='utf-8') as wenjian:
            self.json_data = json.load(wenjian)
        self.json_data_original = self.json_data.copy()
        return self.json_data
    
    def save_json(self,**kargs):
        # 这个是保存json文件
        if "location" in kargs:
            location = kargs["location"]
        else:
            location = self.json_location
        with open(location, 'w', encoding='utf-8') as wenjian:
            json.dump(self.json_data,wenjian,ensure_ascii=False,indent=4)
        return 0
    
    # 然后是琢磨一下需要哪些编辑方法
    def set_commands(self, command_list:list):
        # print("set_commands: unfinished yet")
        # 首先把这些个command加入到queue里面去。增加一个键值对，当前时间。
        for comand_single in command_list:
            comand_single["step_num"] = self.num
            self.commands_queue.put(comand_single)
        # 这个是调度一下，到底执行哪种编辑方法。
        # 然后开始执行，具体的逻辑还得想想。
        # 拿出第一个，如果是这一步的，就给它执行了，如果不是，就结束退出。

        for i in range(114514): # 原则上这里应该是个while，但是保险起见防止死循环。
            if len(self.commands_queue.queue)==0:
                return # 没有什么命令，直接溜了溜了。
        
            # 看一下第一个
            comand_single = self.commands_queue.queue[0]
            if comand_single["step_num"] <= self.num:
                # 执行
                comand_single = self.commands_queue.get()
                self.set_commands_single(comand_single)

        pass

    def set_commands_single(self,comand_single):
        # 这个是真的要开始解析命令了。
        obj_id = comand_single["obj_id"]
        if comand_single["type"] == "add":
            pass          
        elif comand_single["type"] == "delete":
            pass 
        else:
            raise Exception("undefined comand type in set_commands_single, G.")
    
    def command_add(self, unit_type, team_ID):
        # 逻辑应该是这样的，检验里面有多少个这种单位，然后随机找一个复制一下，改改ID和team_ID
        # 防止删没了，所以先复制一份。# 不随机了，直接加就完事儿了
        same_num = 0
        unit_reserve = None
        for unit_ID in self.json_data["UnitState"]:
            unit = self.json_data["UnitState"][unit_ID]
            if unit["UnitType"] == unit_type and self.check_team(unit,team_ID):
                same_num += 1
            if same_num ==1:
                # 直接存一个，后面就照着这个来了。
                unit_reserve = unit
        
        add_ID = unit_type +"_"+ str(same_num)
        self.json_data["UnitState"][add_ID] = unit_reserve
        pass
    
    def command_delete(self, unit_type,team_ID):
        # 删除一个这种类型的单位。还是得检测队伍ID，不然有可能删岔了。
        # 还是讲究一点，从后往前删除可能会比较好一些。
        same_num = 0
        unit_ID_delete = None
        for unit_ID in self.json_data["UnitState"]:
            unit = self.json_data["UnitState"][unit_ID]
            if unit["UnitType"] == unit_type and self.check_team(unit,team_ID):
                same_num += 1
                unit_ID_delete = unit_ID # 一直刷，刷到符合要求的最后一个
        
        if same_num > 0: 
            # 没删完，就删一个。
            delete_ID = unit_ID_delete
            del self.json_data["UnitState"][delete_ID]
        else:
            # 删完了，就算了
            # print("no unit to delete")
            pass
        pass
    
    def check_team(self,unit,team_ID):
        # 检查一下这个单位是不是这个队的和team_ID是否兼容
        if unit["PlayerName"] == "redPlayer" and team_ID=="0":
            flag = True
        elif unit["PlayerName"] == "bluePlayer" and team_ID=="1":
            flag = True
        else:
            flag = False
        return flag
    
    def check_compatibility(self,unit_type,team_ID):
        # 检查一下这个单位类型和team_ID是否兼容
        # 要是不兼容，就照着unit_type来改team_ID.
        flag = True
        if unit_type == "MainBattleTank_ZTZ100" and team_ID=="1" :
            # 蓝方没有这个单位，所以不兼容，强行改
            flag = False
            team_ID = "0"
        elif unit_type == "MainBattleTank_ZTZ200" and team_ID=="0":
            flag = False
            team_ID = "1"     
        elif unit_type == "WheeledCmobatTruck_ZB100" and team_ID =="1":
            flag = False
            team_ID = "0"
        elif unit_type == "WheeledCmobatTruck_ZB200" and team_ID =="0":
            flag = False
            team_ID = "1"
        elif unit_type == "Howitzer_C100" and team_ID =="1":
            flag = False
            team_ID = "0"
        elif unit_type == "Howitzer_C200" and team_ID =="0":
            flag = False
            team_ID = "1"
        elif unit_type == "ArmoredTruck_ZTL100" and team_ID =="1":
            flag = False
            team_ID = "0"
        elif unit_type == "ArmoredTruck_ZTL200" and team_ID =="0":
            flag = False
            team_ID = "1"
        return flag, unit_type, team_ID

if __name__ == "__main__":
    shishi_json = json_editor()
    shishi_json.set_location(r"C:\Users\42418\Desktop\2024ldjs\EnglishMulu\test_scene\auto_test\new1.Json")
    shishi_json.load_json()
    shishi_json.command_add("MainBattleTank_ZTZ100",team_ID="0")
    shishi_json.command_delete("MainBattleTank_ZTZ200",team_ID="1")
    shishi_json.save_json(location = r"C:\Users\42418\Desktop\2024ldjs\EnglishMulu\test_scene\auto_test\new1_gai.Json")
 