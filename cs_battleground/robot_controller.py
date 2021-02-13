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
                repeat_on_hold=True,
            ),
            KeyHandler(
                'w+d',
                press=self.turn_right,
                repeat_on_hold=True,
            ),
            KeyHandler(
                's+a',
                press=self.backward_turn_left,
                repeat_on_hold=True,
            ),
            KeyHandler(
                's+d',
                press=self.backward_turn_right,
                repeat_on_hold=True,
            ),
            KeyHandler(
                'w',
                press=self.forward,
                release=self.stop,
                repeat_on_hold=True,
            ),
            KeyHandler(
                'a',
                release=self.stop,
                repeat_on_hold=True,
            ),
            KeyHandler(
                's', press=self.backward,
                release=self.stop,
                repeat_on_hold=True,
            ),
            KeyHandler(
                'd',
                release=self.stop,
                repeat_on_hold=True,
            ),

            *(
                key_handlers
                if key_handlers
                else ()
            )
        ]) as handler:
            handler.join()
