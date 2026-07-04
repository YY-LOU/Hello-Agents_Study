""" 编写tool工具并调用 """

from typing import Any, Dict
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()



import requests


def search_weather(city: str) -> str:
    """搜索城市city的天气"""
    req=requests.get(f"https://wttr.in/{city}?format=%C+%t") # 调用wttr.in API获取天气信息
    print(req) # 打印请求信息
    return req

""" 构建通用的工具执行器
当智能体需要使用多种工具时（例如，除了搜索，还可能需要计算、查询数据库等），
我们需要一个统一的管理器来注册和调度这些工具。
为此，我们创建一个 ToolExecutor 类 """
class ToolExecutor:
    """ 一个工具执行器负责管理和执行工具 """
    def __init__(self):
        self.tools:Dict[str,Dict[str,Any]]={}
    
    def register_tool(self, tool_name: str,description:str, func:callable):
        """ 向工具箱中注册一个工具 """
        if tool_name in self.tools:
            raise Exception(f"Tool {tool_name} already registered")
        self.tools[tool_name] = {
            "description":description,
            "func":func
        }
        print(f"工具： {tool_name} 已注册")

    def getTool(self,tool_name: str)->callable:
        """ 根据工具名称获取工具的执行函数"""
        if tool_name not in self.tools:
            raise Exception(f"Tool {tool_name} not found")
        return self.tools.get(tool_name,{}).get("func")
    
    def getToolsDescription(self)->str:
        """ 获取所有工具的描述 """
        return "\n".join(
            [f"{tool_name}: {tool_desc}" for tool_name,tool_desc in self.tools.items()
        ])

""" 测试 """
if __name__=='__main__':
    # 创建工具执行器并初始化
    executor=ToolExecutor()
    # 注册工具
    executor.register_tool("search_weather","搜索城市天气的工具，只需参数:城市名",search_weather)
    # 打印所有可用的工具
    print(executor.getToolsDescription())
    
    # 注册DEEPSEEK请求客户端
    client=OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASEURL")
    )

    # 调用DEEPSEEK模型
    response=client.chat.completions.create(
        model=os.getenv("DEEPSEEK_MODEL"),
        messages=[
            {"role":"user","content":"你好，帮我查一下桐梓县天气"}
        ],
        tools=executor.tools
    )

    print(response.choices[0].message.content)




