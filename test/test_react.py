#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/15 17:13
# @Author  : wang ke
# @File    : test_react.py
# @Software: PyCharm

import os
from dotenv import load_dotenv
import serpapi

from tools.registry import ToolRegistry

load_dotenv()


def search(query: str) -> str:
    """
    一个基于SerpApi的实战网页搜索引擎工具。
    它会智能地解析搜索结果，优先返回直接答案或知识图谱信息。
    """
    print(f"🔍 正在执行 [SerpApi] 网页搜索: {query}")
    try:
        search = serpapi.search(
            q=query,
            engine="google",
            api_key=os.getenv("SERPAPI_API_KEY"),
            num=3
        )

        results = search.as_dict()

        # 智能解析:优先寻找最直接的答案
        if "answer_box_list" in results:
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results and "answer" in results["answer_box"]:
            return results["answer_box"]["answer"]
        if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
            return results["knowledge_graph"]["description"]
        if "organic_results" in results and results["organic_results"]:
            # 如果没有直接答案，则返回前三个有机结果的摘要
            snippets = [
                f"[{i + 1}] {res.get('title', '')}\n{res.get('snippet', '')}"
                for i, res in enumerate(results["organic_results"][:3])
            ]
            return "\n\n".join(snippets)

        return f"对不起，没有找到关于 '{query}' 的信息。"

    except Exception as e:
        return f"搜索时发生错误: {e}"


def demo_search_tool():
    # 1. 初始化工具执行器
    toolExecutor = ToolRegistry()

    # 2. 注册我们的实战搜索工具
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    toolExecutor.register_function("Search", search_description, search)

    # 3. 打印可用的工具
    print("\n--- 可用的工具 ---")
    print(toolExecutor.get_tools_description())

    # 4. 智能体的Action调用，这次我们问一个实时性的问题
    print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
    tool_name = "Search"
    tool_input = "英伟达最新的GPU型号是什么"

    observation = toolExecutor.execute_tool(tool_name, tool_input)

    print("--- 观察 (Observation) ---")
    print(observation)

def demo_react_agent():
    from agents.react_agent import ReActAgent
    from core.llm import AgentsLLM

    # 初始化 LLM
    llm = AgentsLLM()

    # 初始化工具注册表并注册搜索工具
    tool_registry = ToolRegistry()
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"

    tool_registry.register_function("Search", search_description, search)

    # 创建 ReAct 智能体
    agent = ReActAgent(
        name="react-agent-demo",
        llm=llm,
        tool_registry=tool_registry,
        max_steps=5
    )

    # 运行智能体，提出一个需要实时信息的问题
    question = "华为最新手机型号及主要卖点？"
    answer = agent.run(question)

    print("\n--- 最终答案 ---")
    print(answer)

# --- 工具初始化与使用示例 ---
if __name__ == '__main__':
    # 运行搜索工具示例
    # demo_search_tool()

    # 运行 ReAct 智能体示例
    demo_react_agent()



