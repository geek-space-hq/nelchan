from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TopicChannelLog:
    action: str
    channel_id: str
    message_id: str
    executed_user_id: str
    created_at: datetime
    topic_title: Optional[str] = None
