from abc import ABC, abstractmethod

from keyboard_handler import KeyboardHandler


class RobotController(ABC):
    def _move(self):
        ...

    @abstractmethod
    def forward(self):
        ...

    @abstractmethod
    def backward(self):
        ...

    @abstractmethod
    def right(self):
        ...

    @abstractmethod
    def left(self):
        ...

    @abstractmethod
    def backward_right(self):
        ...

    @abstractmethod
    def backward_left(self):
        ...

    @abstractmethod
    def stop(self):
        ...


def start_control_session(
    controller: RobotController,
    additional_press_handlers: dict = None,
    additional_release_handlers: dict = None,
):
    default_movement_press_handlers = {
        'w+a': controller.left,
        'w+d': controller.right,
        's+a': controller.backward_left,
        's+d': controller.backward_right,
        'w': controller.forward,
        's': controller.backward,
        'd': controller.stop,
    }
    default_movement_release_handlers = {
        'w': controller.stop,
        'a': controller.stop,
        's': controller.stop,
        'd': controller.stop,
    }
    with KeyboardHandler(
        {
            **default_movement_press_handlers,
            **(
                additional_press_handlers
                if additional_press_handlers
                else {}
            )
        },
        {
            **default_movement_release_handlers,
            **(
                additional_release_handlers
                if additional_release_handlers
                else {}
            )
        },
    ) as handler:
        handler.join()
