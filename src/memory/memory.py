from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from typing import Dict, List, Optional

class Message(BaseModel):
    """消息模型"""
    role: str
    content: str

class GroupMemory(BaseModel):
    """群组记忆类"""
    chat_id: int  # 改用 chat_id 而不是 group_id
    messages: List[Message] = []
    max_messages: int = 10
    memory: Optional[ConversationBufferMemory] = None

    def __init__(self, chat_id: int, **data):
        super().__init__(chat_id=chat_id, **data)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    def add_message(self, role: str, content: str):
        """添加新消息"""
        # 添加新消息
        self.messages.append(Message(role=role, content=content))
        
        # 如果超过最大消息数，删除最旧的消息
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
        
        # 更新 LangChain 记忆
        if role == "human":
            self.memory.save_context(
                {"input": content}, 
                {"output": ""}
            )
        elif role == "assistant":
            # 更新最后一条记录的输出
            history = self.memory.load_memory_variables({})
            if history and "chat_history" in history:
                last_interaction = history["chat_history"][-1]
                last_interaction.output = content

    def get_messages(self) -> List[Message]:
        """获取所有消息"""
        return self.messages

    def clear(self):
        """清空记忆"""
        self.messages = []
        self.memory.clear() 