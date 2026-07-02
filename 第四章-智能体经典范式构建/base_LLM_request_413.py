""" 
    Hello-agents教程文档4.1.3部分 
    使用基础的request包请求LLM
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List,Dict
import deepseek

# 先加载环境
load_dotenv()

class HelloAgents:
    """ 定义Hello Agents LLM客户端，内部定义模型，API调用功能 """
    def __init__(self,model:str=None,api_key:str=None,base_url:str=None):
        """ 初始化函数，创建OpenAI对象client"""
        self.model=model or os.getenv("DEEPSEEK_MODEL")
        self.api_key=api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url=base_url or os.getenv("DEEPSEEK_BASEURL")

        if not all([model,api_key,base_url]):
            print("请确保model,api_key,base_url都不为空")
            print([model,api_key,base_url])
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")
        
        # 定义openAI格式的client
        # 不需要在client处穿model参数
        self.client=OpenAI(api_key=self.api_key,base_url=self.base_url)
    
    def think(self,messages:List[Dict[str,str]]):
        """ 通过API调用LLM并返回str类型数据 """
        response=self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            stream=True
        )
        collect_content=[]
        for chunk in response:
            if not chunk.choices:
                continue
            if chunk.choices[0].delta.reasoning_content!=None:
                print(chunk.choices[0].delta.reasoning_content,end="")
            elif chunk.choices[0].delta.content!=None:
                if collect_content is []:
                    print("\n")
                print(chunk.choices[0].delta.content,end="")
                collect_content.append(chunk.choices[0].delta.content)
        
    
if __name__=='__main__':
    # 创建client对象并初始化
    llm_client=HelloAgents(
        model=os.getenv("DEEPSEEK_MODEL"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASEURL")
    )

    # 硬编码给出示例messages
    messages=[
        {
            "role":"user",
            "content":"你好，我叫yy"
        },
        {
            "role":"system",
            "content":"你是一个善于思考的助理，请用中文回答我的问题。"
        }
    ]

    # 调用请求
    res=llm_client.think(messages=messages)
    print(res)


    
