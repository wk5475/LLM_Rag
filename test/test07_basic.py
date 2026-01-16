#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/15 10:26
# @Author  : wang ke
# @File    : test07_basic.py
# @Software: PyCharm

from core.llm import AgentsLLM
from agents.simple_agent import SimpleAgent

def demo_simple_agent():
    """演示SimpleAgent - 基础对话"""
    print("\n" + "="*60)
    print("🤖 SimpleAgent 演示 - 基础对话Agent")
    print("="*60)

    # 创建LLM实例
    llm = AgentsLLM()

    # 创建简单Agent
    agent = SimpleAgent(
        name="助手",
        llm=llm,
        system_prompt="你是一个有用的AI助手，请用中文回答问题。"
    )

    # 测试对话
    test_questions = [
        "你好，请介绍一下自己"
    ]

    for question in test_questions:
        print(f"\n用户: {question}")
        try:
            response = agent.run(question)
            print(f"助手: {response}")
        except Exception as e:
            print(f"❌ 错误: {e}")

if __name__ == "__main__":
    demo_simple_agent()