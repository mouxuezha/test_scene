# 这个暂时就别来什么窗口对话啥的了，就直接读命令行了。那些要是要的话后面再给它加。
import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from support.tools import *
from model_communication.model_comm_langchain import ModelCommLangchain
from text_scene.prompts import *
from text_scene.text_transfer import text_transfer
from json_editor.json_editor import json_editor

class auto_run():
    def __init__(self, Comm_type ="duizhan"):
        self.LLM_model = "zhipu" # 这里可以改，默认是qianfan,还有智谱啥的
        self.location = r"auto_test"
        
        self.timestep = 0 

        self.model_communication = ModelCommLangchain(model_name=self.LLM_model,Comm_type=Comm_type)
        self.text_transfer = text_transfer()
        self.json_editor = json_editor()
        self.json_editor.set_location(self.location + r"\new1.Json")
        
        pass

    def run(self):
        pass

    def run_one_step(self, additional_str = ""):
        # 先是得到当前的态势
        jieguo = self.text_transfer.status_to_text(self.json_editor.json_data)

        # 然后获取一下人类意图.
        human_intent = self.human_intervene_check(jieguo)

        # 然后组装一下，就可以考虑给大模型发过去了。
        all_str = "当前态势：" + jieguo + "\n" + "人类意图：" + human_intent + "\n" + additional_str + "\n 请按照之前约定的格式给出指令。" 

        response_str = self.model_communication.communicate_with_model(all_str)

        # 然后根据大模型的输出，先把修改json的命令转化出来。
        commands = self.text_transfer.text_to_commands(response_str)

        # 把提取出来的命令发给json_editor，让它里面设定抽象状态啥的
        self.json_editor.set_commands(commands) # 得专门给它定制一个发命令的才行，不然不行。
        pass

    def run_one_step_shadow(self):
        # 这个好像是比较不需要的，因为生成场景是之前就弄好的。
        pass 
        


    def main_loop(self, **kargs):
        # 这个就是主循环呗。
        self.timestep = 0 # 每个episode的步数
        log_file = auto_save_file_name(log_folder=r'auto_test')
        self.json_editor.load_json(file_name="auto_test/scene.json")
        print("begin main loop")

        while True:
            # 检测人是不是满意了，人如果满意就给个退出信息。唯一的用户行为就是这个吧。
            self.run_one_step()
    
    def human_intervene_check(self,status_str):
        # 这个是最简单的人机互动，就不要dialog_box了，直接来罢
        print("当前态势" + status_str + "=========================\n")
        print("请输入场景编辑指令：")
        human_intent = input()
        return human_intent