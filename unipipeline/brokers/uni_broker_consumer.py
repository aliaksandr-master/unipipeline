from typing import NamedTuple, Callable, Awaitable

from unipipeline.brokers.uni_broker_message_manager import UniBrokerMessageManager
from unipipeline.message_meta.uni_message_meta import UniMessageMeta


class UniBrokerConsumer(NamedTuple):
    topic: str
    id: str
    group_id: str
    unwrapped: bool
    message_handler: Callable[[UniMessageMeta, UniBrokerMessageManager], Awaitable[None]]