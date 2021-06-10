from dataclasses import dataclass


@dataclass
class TopicChannel:
    channel_id: str
    guild_id: str
    topic_allocated: bool = False
