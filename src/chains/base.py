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

class BaseChain:
    def __init__(self, memory=None):
        # 配置 Google Gemini
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        # 创建 LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.7,
            max_tokens=2048,
            google_api_key=Config.GEMINI_API_KEY,
        )
        
        # 设置工具
        self.tools = [
            CryptoPriceTool(),
            CryptoAnalysisTool()
        ]
        
        # 设置记忆
        self.memory = memory or ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 创建代理
        prompt = self._create_prompt()
        self.agent = create_react_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            return_intermediate_steps=False,
            output_key="output",
            max_iterations=1,  # 限制最大迭代次数
            max_execution_time=10.0  # 最大执行时间（秒）
        )

    def _create_prompt(self):
        return PromptTemplate(
            input_variables=["chat_history", "input", "agent_scratchpad", "tool_names", "tools"],
            template=self._get_template()
        )

    def _get_template(self):
        raise NotImplementedError

    async def run(self, input_text):
        """运行代理并返回结果"""
        try:
            result = await self.agent_executor.ainvoke({"input": input_text})
            return result.get("output", "抱歉，我现在无法处理这个请求。")
        except Exception as e:
            print(f"Error in agent execution: {e}")
            return "抱歉，处理您的请求时出现了错误。请稍后再试。" 