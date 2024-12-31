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

logger = logging.getLogger(__name__)

class BaseChain:
    def __init__(self, memory=None):
        # 配置 Google Gemini
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        # 创建 LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
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
            memory=self.memory,  # 使用 memory 属性
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=2,
            max_execution_time=None,
        )

    async def run(self, input_text):
        """运行代理并返回结果"""
        try:
            # 添加重试逻辑
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
                        
                    return "抱歉，我现在无法理解这个请求。"
                    
                except Exception as e:
                    logger.error(f"Error in attempt {attempt + 1}", exc_info=True)
                    if attempt == max_retries - 1:
                        raise
            
            return "抱歉，我现在无法处理这个请求。"
            
        except Exception as e:
            logger.error("Final error", exc_info=True)
            return "抱歉，处理您的请求时出现了错误。请稍后再试。"

    def _create_prompt(self):
        return PromptTemplate(
            input_variables=["chat_history", "input", "agent_scratchpad", "tool_names", "tools"],
            template=self._get_template()
        )

    def _get_template(self):
        raise NotImplementedError 