#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/12 13:59
# @Author  : wang ke
# @File    : test_chain.py
# @Software: PyCharm

from tools.chain import ToolChain

# 便捷函数
def create_research_chain() -> ToolChain:
    """创建一个研究工具链：搜索 -> 计算 -> 总结"""
    chain = ToolChain(
        name="research_and_calculate",
        description="搜索信息并进行相关计算"
    )

    # 步骤1：搜索信息
    chain.add_step(
        tool_name="search",
        input_template="{input}",
        output_key="search_result"
    )

    # 步骤2：基于搜索结果进行计算
    chain.add_step(
        tool_name="my_calculator",
        input_template="2 + 2",  # 简单的计算示例
        output_key="calc_result"
    )

    return chain


def create_simple_chain() -> ToolChain:
    """创建一个简单的工具链示例"""
    chain = ToolChain(
        name="simple_demo",
        description="简单的工具链演示"
    )

    # 只包含一个计算步骤
    chain.add_step(
        tool_name="my_calculator",
        input_template="{input}",
        output_key="result"
    )

    return chain

if __name__ == "__main__":
    from tools.registry import ToolRegistry
    from tools.my_tools.my_calculator_tool import my_calculate
    from tools.my_tools.my_advanced_search import MyAdvancedSearchTool

    registry = ToolRegistry()

    registry.register_function(
        name="my_calculator",
        description="简单的数学计算工具，支持基本运算(+,-,*,/)和sqrt函数",
        func=my_calculate
    )

    # 创建搜索工具实例
    search_tool = MyAdvancedSearchTool()

    # 注册搜索工具的方法作为函数
    registry.register_function(
        name="search",
        description="高级搜索工具，整合Tavily和SerpAPI多个搜索源，提供更全面的搜索结果",
        func=search_tool.search
    )


    # chain = create_simple_chain()
    chain = create_research_chain()
    result = chain.execute(registry, "2 + 2 * 3")
    print(result)
