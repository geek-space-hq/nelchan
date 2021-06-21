from dataclasses import dataclass
from typing import Optional


@dataclass
class TopicChannelLog:
    action: str
    channel_id: str
    message_id: str
    executed_user_id: str
    topic_title: Optional[str] = None
