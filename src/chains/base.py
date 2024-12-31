from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import ReActJsonSingleInputOutputParser
import google.generativeai as genai
from ..bot.config import Config
from ..tools import CryptoPriceTool, CryptoAnalysisTool
from typing import Dict, Any, Optional
import logging
import re

logger = logging.getLogger(__name__)

class BaseChain:
    def __init__(self, memory=None):
        # 配置 Google Gemini
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        # 创建 LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-exp-1206",
            temperature=0.3,
            max_tokens=2048,
            google_api_key=Config.GEMINI_API_KEY,
        )
        
        # 设置工具
        self.tools = [
            CryptoPriceTool(),
            CryptoAnalysisTool()
        ]
        
        # 使用传入的记忆或创建新的
        self.memory = memory.memory if memory else ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 创建代理
        prompt = self._create_prompt()
        logger.info("=== Prompt Template ===")
        logger.info(prompt.template)
        
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # 配置执行器
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=2,
            max_execution_time=None,
        )

    async def run(self, input_text):
        """运行代理并返回结果"""
        try:
            # 检查是否需要使用工具
            if not self._needs_tools(input_text):
                # 直接使用 LLM 回答
                response = await self._direct_response(input_text)
                return response
            
            # 使用代理处理需要工具的请求
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    logger.info(f"=== Attempt {attempt + 1} ===")
                    logger.info(f"Input Text: {input_text}")
                    
                    # 获取当前记忆内容
                    memory_vars = self.memory.load_memory_variables({})
                    logger.info("\n--- Current Memory ---")
                    if "chat_history" in memory_vars:
                        chat_history = memory_vars["chat_history"]
                        logger.info("Chat History:")
                        for msg in chat_history:
                            logger.info(f"{msg.type}: {msg.content}")
                    
                    # 执行代理
                    result = await self.agent_executor.ainvoke(
                        {
                            "input": input_text,
                            "chat_history": memory_vars.get("chat_history", []),
                        }
                    )
                    
                    logger.info("\n--- Agent Result ---")
                    logger.info(f"Output: {result.get('output', 'No output')}")
                    if "intermediate_steps" in result:
                        logger.info(f"Steps: {result['intermediate_steps']}")
                    
                    if isinstance(result, dict) and "output" in result:
                        logger.info("\n--- Final Output ---")
                        logger.info(result["output"])
                        return result["output"]
                    
                except Exception as e:
                    logger.error(f"Error in attempt {attempt + 1}", exc_info=True)
                    if attempt == max_retries - 1:
                        raise
            
            return "抱歉，我现在无法处理这个请求。"
            
        except Exception as e:
            logger.error("Final error", exc_info=True)
            return "抱歉，处理您的请求时出现了错误。请稍后再试。"

    def _needs_tools(self, input_text: str) -> bool:
        """检查是否需要使用工具"""
        # 检查是否包含加密货币相关关键词
        crypto_keywords = [
            'btc', 'bitcoin', '比特币',
            'eth', 'ethereum', '以太坊',
            '价格', 'price', '分析', 'analysis',
            '走势', '市场', 'market',
            '币', 'coin', 'crypto'
        ]
        
        return any(keyword in input_text.lower() for keyword in crypto_keywords)

    async def _direct_response(self, input_text: str) -> str:
        """直接使用 LLM 回答"""
        try:
            # 创建简单的提示模板
            template = """你是一个友好的群聊助手。请用简洁的语言回答用户的问题。

用户输入：{input}

请回答："""
            
            prompt = PromptTemplate(
                template=template,
                input_variables=["input"]
            )
            
            # 创建简单的链
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            # 获取回答
            response = await chain.arun(input=input_text)
            
            # 清理回答（移除多余的换行等）
            response = re.sub(r'\n+', '\n', response).strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Error in direct response: {e}", exc_info=True)
            return "抱歉，我现在无法回答这个问题。"

    def _create_prompt(self):
        return PromptTemplate(
            input_variables=["chat_history", "input", "agent_scratchpad", "tool_names", "tools"],
            template=self._get_template()
        )

    def _get_template(self):
        raise NotImplementedError 