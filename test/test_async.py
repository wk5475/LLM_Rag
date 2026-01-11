#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/12 11:04
# @Author  : wang ke
# @File    : test_async.py
# @Software: PyCharm

from dotenv import load_dotenv

from tools.registry import ToolRegistry
from tools.my_tools.my_advanced_search import MyAdvancedSearchTool
from tools.my_tools.my_calculator_tool import my_calculate
from tools.async_tool_executor import AsyncToolExecutor

# 加载环境变量
load_dotenv()

# 使用示例
async def test_parallel_execution():
    """测试并行工具执行"""
    registry = ToolRegistry()

    # 创建搜索工具实例
    search_tool = MyAdvancedSearchTool()

    # 注册搜索工具的方法作为函数
    registry.register_function(
        name="search",
        description="高级搜索工具，整合Tavily和SerpAPI多个搜索源，提供更全面的搜索结果",
        func=search_tool.search
    )

    registry.register_function(
        name="my_calculator",
        description="简单的数学计算工具，支持基本运算(+,-,*,/)和sqrt函数",
        func=my_calculate
    )

    executor = AsyncToolExecutor(registry)

    # 定义并行任务
    tasks = [
        {"tool_name": "search", "input_data": "Python编程"},
        {"tool_name": "search", "input_data": "机器学习"},
        {"tool_name": "my_calculator", "input_data": "2 + 2"},
        {"tool_name": "my_calculator", "input_data": "sqrt(16)"},
    ]

    # 并行执行
    results = await executor.execute_tools_parallel(tasks)

    for i, result in enumerate(results):
        print(f"任务 {i+1} 结果: {result[:100]}...")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_parallel_execution())