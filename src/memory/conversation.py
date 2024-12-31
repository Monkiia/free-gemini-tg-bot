from langchain.memory import ConversationBufferWindowMemory
from datetime import datetime
from typing import Set, Optional, List, Dict, Any
from pydantic import BaseModel, Field

class GroupStats(BaseModel):
    """群组统计信息模型"""
    group_id: int = Field(description="群组ID")
    emotions: List[Dict] = Field(default_factory=list, description="情绪历史")
    message_count: int = Field(default=0, description="消息计数")
    active_users: Set[int] = Field(default_factory=set, description="活跃用户ID集合")
    last_activity: Optional[datetime] = Field(default=None, description="最后活动时间")

    class Config:
        arbitrary_types_allowed = True

class GroupMemory(ConversationBufferWindowMemory):
    """群组记忆类，用于存储群组的对话历史和统计信息"""

    def __init__(self, group_id: int, k: int = 10):
        super().__init__(k=k, return_messages=True, memory_key="chat_history")
        self._group_id = group_id
        self._emotions = []
        self._message_count = 0
        self._active_users = set()
        self._last_activity = None

    @property
    def group_id(self) -> int:
        return self._group_id

    @property
    def stats(self) -> dict:
        """获取群组统计信息"""
        return {
            "group_id": self._group_id,
            "message_count": self._message_count,
            "active_users_count": len(self._active_users),
            "last_activity": self._last_activity,
            "emotions_count": len(self._emotions)
        }

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        """保存对话上下文和更新统计信息"""
        super().save_context(inputs, outputs)
        self._message_count += 1
        self._last_activity = datetime.now()
        if "user_id" in inputs:
            self._active_users.add(inputs["user_id"])

    def add_emotion(self, emotion: str, timestamp: Optional[datetime] = None) -> None:
        """添加情绪记录"""
        self._emotions.append({
            "emotion": emotion,
            "timestamp": timestamp or datetime.now()
        })

    def get_emotions(self) -> List[Dict]:
        """获取情绪历史"""
        return self._emotions.copy()

    def get_active_users(self) -> Set[int]:
        """获取活跃用户集合"""
        return self._active_users.copy()

    def clear(self) -> None:
        """清除所有记忆和统计信息"""
        super().clear()
        self._emotions = []
        self._message_count = 0
        self._active_users = set()
        self._last_activity = None

    def to_dict(self) -> dict:
        """将记忆转换为字典格式"""
        return {
            "memory": super().dict(),
            "stats": {
                "group_id": self._group_id,
                "emotions": self._emotions,
                "message_count": self._message_count,
                "active_users": list(self._active_users),
                "last_activity": self._last_activity
            }
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GroupMemory":
        """从字典格式恢复记忆"""
        instance = cls(group_id=data["stats"]["group_id"])
        instance._emotions = data["stats"]["emotions"]
        instance._message_count = data["stats"]["message_count"]
        instance._active_users = set(data["stats"]["active_users"])
        instance._last_activity = data["stats"]["last_activity"]
        
        # 恢复记忆内容
        for key, value in data["memory"].items():
            setattr(instance, key, value)
        return instance 