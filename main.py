

import os

from pathlib import Path

from utils.log import get_logger
from config import RAGConfig, DEFAULT_CONFIG
from rag_modules.data_preparation import DataPreparationModule
from rag_modules.index_construction import IndexConstructionModule
from rag_modules.retrieval_optimization import RetrievalOptimizationModule
from rag_modules.generation_integration import GenerationIntegrationModule


logger = get_logger()


class RecipeRAGSystem:
    """Drink RAG系统主类"""

    def __init__(self, config: RAGConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.data_module = None
        self.index_module = None
        self.retrieval_module = None
        self.generation_module = None

        # 检查数据路径
        if not Path(self.config.data_path).exists():
            raise FileNotFoundError(f"数据路径不存在: {self.config.data_path}")


    def initialize_system(self):
        """初始化所有模块"""
        # 1. 初始化数据准备模块
        self.data_module = DataPreparationModule(self.config.data_path)
        logger.info("数据准备模块初始化完成.")

        # 2. 初始化索引构建模块
        self.index_module = IndexConstructionModule(
            model_path=self.config.embedding_model,
            index_save_path=self.config.index_save_path
        )
        logger.info("索引构建模块初始化完成.")

        # 3. 初始化生成集成模块
        self.generation_module = GenerationIntegrationModule(
            model_name=self.config.llm_model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        logger.info("生成集成模块初始化完成.")

    def build_knowledge_base(self):
        """构建知识库"""
        # 1. 尝试加载已保存的索引
        vectorstore = self.index_module.load_index()

        if vectorstore is not None:
            # 加载已有索引，但仍需要文档和分块用于检索模块
            self.data_module.load_documents()
            chunks = self.data_module.chunk_documents()
        else:
            # 构建新索引的完整流程
            self.data_module.load_documents()
            chunks = self.data_module.chunk_documents()
            vectorstore = self.index_module.build_vector_index(chunks)
            self.index_module.save_index()

        # 初始化检索优化模块
        self.retrieval_module = RetrievalOptimizationModule(vectorstore, chunks)

    def ask_question(self, question: str, stream: bool = False):
        """回答用户问题"""
        # 1. 查询路由
        route_type = self.generation_module.query_router(question)

        # 2. 智能查询重写（根据路由类型）
        if route_type == 'list':
            rewritten_query = question  # 列表查询保持原样
        else:
            rewritten_query = self.generation_module.query_rewrite(question)

        # 3. 检索相关子块
        relevant_chunks = self.retrieval_module.hybrid_search(rewritten_query, top_k=self.config.top_k)

        # 4. 根据路由类型选择回答方式
        if route_type == 'list':
            # 列表查询：返回菜品名称列表
            relevant_docs = self.data_module.get_parent_documents(relevant_chunks)
            return self.generation_module.generate_list_answer(question, relevant_docs)
        else:
            # 详细查询：获取完整文档并生成详细回答
            relevant_docs = self.data_module.get_parent_documents(relevant_chunks)

            if route_type == "detail":
                # 详细查询使用分步指导模式
                return self.generation_module.generate_step_by_step_answer(question, relevant_docs)
            else:
                # 一般查询使用基础回答模式
                return self.generation_module.generate_basic_answer(question, relevant_docs)

    def run_interactive(self):
        """运行交互式问答"""
        print("=" * 60)
        print("🍽️  酒鬼 RAG系统 - 交互式问答  🍽️")
        print("=" * 60)

        # 初始化系统和构建知识库
        self.initialize_system()
        self.build_knowledge_base()

        while True:
            print("\n请输入您的问题:")
            user_input = input().strip()
            if user_input.lower() in ['退出', 'quit', 'exit']:
                break

            # 询问是否使用流式输出
            stream_choice = input("是否使用流式输出? (y/n, 默认y): ").strip().lower()
            use_stream = stream_choice != 'n'

            if use_stream:
                # 流式输出，实时显示生成过程
                for chunk in self.ask_question(user_input, stream=True):
                    print(chunk, end="", flush=True)
            else:
                # 普通输出
                answer = self.ask_question(user_input, stream=False)
                print(answer)

if __name__ == "__main__":

    drink_rag_system = RecipeRAGSystem()

    drink_rag_system.run_interactive()