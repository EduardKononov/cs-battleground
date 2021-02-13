from abc import ABC, abstractmethod
from typing import Sequence, Optional

from cs_battleground.keyboard_whatcher import KeyboardWatcher, KeyHandler

__all__ = ['RobotController']


class RobotController(ABC):
    @abstractmethod
    def forward(self):
        ...

    @abstractmethod
    def turn_right(self):
        ...

    @abstractmethod
    def turn_left(self):
        ...

    @abstractmethod
    def backward(self):
        ...

    @abstractmethod
    def backward_turn_right(self):
        ...

    @abstractmethod
    def backward_turn_left(self):
        ...

    @abstractmethod
    def stop(self):
        ...

    def start_control_session(
        self,
        key_handlers: Optional[Sequence[KeyHandler]] = None,
    ):
        with KeyboardWatcher([
            KeyHandler(
                'w+a',
                press=self.turn_left,
            ),
            KeyHandler(
                'w+d',
                press=self.turn_right,
            ),
            KeyHandler(
                's+a',
                press=self.backward_turn_left,
            ),
            KeyHandler(
                's+d',
                press=self.backward_turn_right,
            ),
            KeyHandler(
                'w',
                press=self.forward,
                release=self.stop,
            ),
            KeyHandler(
                'a',
                release=self.stop,
            ),
            KeyHandler(
                's', press=self.backward,
                release=self.stop,
            ),
            KeyHandler(
                'd',
                release=self.stop,
            ),

            *(
                key_handlers
                if key_handlers
                else ()
            )
        ]) as handler:
            handler.join()
