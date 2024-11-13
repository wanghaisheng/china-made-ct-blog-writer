import lark_oapi as lark  # 飞书后台访问api
from lark_oapi.api.docx.v1 import *  # 飞书后台访问api
import os
from tools.readFromSheet import read_columns  # 从飞书中读取标题表格列表类
from tools.convertFormat import cvt2doc  # 格式转换工具
from generation.generate_articles_async import Generation  # 单篇文章生成类
import time  ## 加入时间库以文章记录生成时间
import threading  ## 加入线程库，同时进行多篇文章生成
import asyncio

from feishu_api.get_tenant_access_token import get_access_token

## 首先进行飞书API的环境变量准备
# 获取飞书后台用户鉴权码 user_access_token
access_token = get_access_token()
# 获取表格token和名称
sheet_token = "YEzAsao9khfQ3BtMAiUclcKznsc"
sheet_name = "爽文短视频"
row_range = "C1:C200"
# 定义记录待生成文章的飞书云表格的相关信息

# 初始化columns对象，以获取表格信息
columns = read_columns(sheet_name, row_range, access_token)
response = columns.readTopicsFromSheet()
title_list = columns.write2variable(response)

# 用filter（）函数剔除为None的title_list子项
title_list = list(filter(lambda x: x is not None, [item for sublist in title_list for item in sublist]))
# 此时title_list已剔除了所有值为None的元素
print(title_list)


# 将编号拼接到字符串列表的每个标题前，以便观察最终批量生产的结果
num_title_list = []
for i, item in enumerate(title_list, 1):
    new_item = f"{i}. {item}"
    num_title_list.append(new_item)

print(num_title_list)

# 记录开始时间
start_time = time.time()
# 实例化一个Generation类
ai_writer = Generation()
# 获取系统和文章提示词
ai_writer.get_system_prompt()
ai_writer.get_article_prompt()



# 定义可以批量生成文章的异步协程请求main函数
async def main(titlelist):
    # 建立协程任务队列
    tasks = []
    for title in titlelist:
        title_name = str(title)
        task = asyncio.create_task(ai_writer.send_to_doubao(title_name))
        tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main(num_title_list))
    cvt2doc("./output","docx")     ## 将md转换为docx格式
    end_time = time.time()
    total_time = end_time - start_time
    print("总响应时间：",total_time)