# 这个暂时就别来什么窗口对话啥的了，就直接读命令行了。那些要是要的话后面再给它加。
import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from support.tools import *
from model_communication.model_comm_langchain import ModelCommLangchain
from text_scene.prompts import *
from text_scene.text_transfer import text_transfer

class auto_run():
    def __init__(self, Comm_type ="duizhan"):
        self.LLM_model = "zhipu" # 这里可以改，默认是qianfan,还有智谱啥的
        
        self.timestep = 0 

        self.model_communication = ModelCommLangchain(model_name=self.LLM_model,Comm_type=Comm_type)
        self.text_transfer = text_transfer()
        
        pass

    def run(self):
        pass

    def run_one_step(self, additional_str = ""):
        # 先是得到当前的态势
        pass

    def run_one_step_shadow(self):
        # 这个好像是比较不需要的，因为生成场景是之前就弄好的。
        pass 
        


    def main_loop(self, **kargs):
        # 这个就是主循环呗。
        self.timestep = 0 # 每个episode的步数
        log_file = auto_save_file_name(log_folder=r'auto_test')

        print("begin main loop")

        while True:
            # 检测人是不是满意了，人如果满意就给个退出信息。唯一的用户行为就是这个吧。
            self.run_one_step()
    