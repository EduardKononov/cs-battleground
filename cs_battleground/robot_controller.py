from abc import ABC, abstractmethod
from typing import Sequence, Optional

from cs_battleground.keyboard_whatcher import KeyboardWatcher, KeyDescriptor

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
        key_handlers: Optional[Sequence[KeyDescriptor]] = None,
    ):
        with KeyboardWatcher([
            KeyDescriptor('w+a', press=self.turn_left),
            KeyDescriptor('w+d', press=self.turn_right),
            KeyDescriptor('s+a', press=self.backward_turn_left),
            KeyDescriptor('s+d', press=self.backward_turn_right),
            KeyDescriptor('w', press=self.forward, release=self.stop),
            KeyDescriptor('a', press=None, release=self.stop),
            KeyDescriptor('s', press=self.backward, release=self.stop),
            KeyDescriptor('d', press=None, release=self.stop),

            *(
                key_handlers
                if key_handlers
                else ()
            )
        ]) as handler:
            handler.join()
