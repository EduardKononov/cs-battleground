import time
from typing import Sequence, Optional

from cs_battleground.keyboard_whatcher import KeyboardWatcher, KeyHandler

__all__ = ['start_control_session']


def start_control_session(key_handlers: Optional[Sequence[KeyHandler]] = None):
    watcher = KeyboardWatcher(key_handlers)
    watcher.start()
