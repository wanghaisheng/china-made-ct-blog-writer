import markdown
import requests
import os
from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime import AsyncArk
import time
import pandas as pd
import lark_oapi as lark
from lark_oapi.api.docx.v1 import *
import json
import asyncio
import subprocess
import threading


class Generation: # 这个类用于读取一连串md文件，并进行

    def __init__ (self):  #  输入一个paper名称列表
        # 设置API密钥，确保已设置好环境变量 ARK_API_KEY
        self.client = AsyncArk(api_key=os.environ.get("ARK_API_KEY"))
        # 原文md中的文本内容
        self.title_name:str = ""
        # 提示词主文件夹名称
        self.prompt_major_folder:str = "./prompts/"
        # 根据平台名称和话题去找提示词文件夹
        self.platform_topic:str = "shorts"
        # 最终提示词文件夹
        self.prompt_folder:str = self.prompt_major_folder+self.platform_topic
        # 科普文章提示词本地名称列表
        # self.article_prompts_filename: list[str] = ["article_intro","article_formal1","article_formal2","article_formal3","article_conclusion"]
        # 爽文短视频提示词本地名称列表
        self.article_prompts_filename: list[str] = ["script_prompt"]
        # 文章提示词列表
        self.article_prompts_content: list[str] = []
        # 文章提示词
        self.article_prompt:str = ""
        # 系统提示词
        self.system_prompt:str = ""
        # 单个列表中单个prompt字符串
        self.prompt_text: str = ""

    # # def get_prompt(self):
    #     # # 获取当前py文件的绝对路径
    #     # current_file_path = os.path.abspath(__file__)
    #     # # 获取当前文件所在的目录路径
    #     # current_directory = os.path.dirname(current_file_path)
    #     # 构造提示词文件夹的路径
    #     print("提示词文件夹为",self.prompt_folder_path)
    #     try:
    #     # 直接获取prompts/文件夹下的内容，不递归遍历子文件夹
    #         for file in os.listdir(self.prompt_folder_path):
    #             file_path = os.path.join(self.prompt_folder_path, file)
    #             if os.path.isfile(file_path) and file.endswith(".md"):
    #                 with open(file_path, 'r') as f:
    #                     self.prompt += f.read() + "\n"  # 读取文件内容并添加到self.prompt变量中，每个文件内容后添加换行符
    #     except FileNotFoundError:
    #         print(f"未找到提示词文件夹 {self.prompt_folder_path}，请检查文件夹是否存在。")
    #     print("提示词为", self.prompt)
    #     return self.prompt
    def get_system_prompt(self):
        with open(self.prompt_folder + "/system_prompt.md", 'r') as f:
            self.system_prompt = f.read()
                
    def get_article_prompt(self):
        for prompt in self.article_prompts_filename:
            with open(self.prompt_folder+'/'+prompt+ '.md', 'r') as f:
                self.article_prompts_content.append(f.read())

    def get_title_from_md(self):
        md_file = self.prompt_folder+ "/title_name.md"
        try:
            with open(md_file, 'r') as f:
                self.title_name = f.read()
                self.title_name.strip()  # 去除前后可能存在的空白字符

        except FileNotFoundError:
            print(f"未找到文件 {md_file}，请检查文件是否存在。")

        return self.title_name
    
    def get_title_from_varible(self,title):
        self.title_name = str(title).strip("['']")
        print("已经成功将变量中提取标题！")
    
    
    # 定义异步多轮对话请求函数（生成整篇文章）
    async def send_to_doubao(self,title_name):
        start_time = time.time()  # 记录开始时间 
        completions = []
        token1_total:int = 0
        token2_prompt:int = 0
        token3_generation:int = 0
        # 在send_to_doubao()内部建立任务队列
        tasks = []

        for index, prompt_content in enumerate(self.article_prompts_content):
            # 创建异步任务来执行generate_paragraph函数
            task = asyncio.create_task(self.generate_paragraph(title_name, prompt_content, completions, index))
            tasks.append(task)

        # 等待所有异步任务完成
        await asyncio.gather(*tasks)

        # 按照索引对生成的段落进行排序
        completions.sort(key=lambda x: x["index"])


        # 定义最终文章存储路径，准备保存文章
        storage_path = title_name + ".md"
        with open("./output/"+storage_path, 'w', encoding='utf-8') as f:
             for paragraph_data in completions:
                f.write(paragraph_data["content"])
        end_time = time.time()  # 记录结束时间
        response_time = end_time - start_time  # 计算响应时间

        print("文章",title_name,"已全部生成！")
        print("文章",title_name,"豆包响应时间为", response_time, "s")
        # print("文章",title_name,"消耗总字符数",token1_total)
        # print("文章",title_name,"提示词消耗总字符",token2_prompt)
        # print("文章",title_name,"生成消耗总字符数",token3_generation)
        return


    # 定义异步单次对话请求函数(生成文章中的一个段落）
    async def generate_paragraph(self, title_name, prompt_content,completions, paragraph_index) -> None:
        # 异步调用大模型，节约等待时间
        completion = await self.client.chat.completions.create(
            model=os.environ.get("endpoint_32kpro"),
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": (title_name + prompt_content)},
            ],
            stream = False
        )

        # 将段落索引和生成的内容组成一个字典，方便后续处理
        paragraph_data = {
            "index": paragraph_index,
            "content": completion.choices[0].message.content
        }
        completions.append(paragraph_data)
        # completions.append(completion.choices[0].message.content)
        print("文章",title_name,"段落生成完毕!")

  
if __name__ == "__main__":
    # 初始化一个类
    ai_writer = Generation()
    ai_writer.get_title_from_md()
    ai_writer.get_system_prompt()
    ai_writer.get_article_prompt()
    ai_writer.send_to_doubao2()
    print("成功写入文本到本地md文件！")

