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
        pass 
    
    def set_location(self,location):
        # 这个是外部设定需要编辑的东西的路径 
        self.json_location = location
        
    def load_json(self):
        # 这个是加载json文件
        with open(self.json_location, 'r', encoding='utf-8') as wenjian:
            self.json_data = json.load(wenjian)
        return self.json_data
    
    def save_json(self):
        # 这个是保存json文件
        with open(self.json_location, 'w', encoding='utf-8') as wenjian:
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
        if comand_single["type"] == "move":
            pass          
        elif comand_single["type"] == "stop":
            pass 
        elif comand_single["type"] == "off_board":
            pass
        else:
            raise Exception("undefined comand type in set_commands_single, G.")
 