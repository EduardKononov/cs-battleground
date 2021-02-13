from typing import Tuple

from cs_battleground.remote_api import client, sim

Orientation = Tuple[float, float, float]

__all__ = ['SimBase']


class SimBase:
    def __init__(self, name: str):
        self.name = name
        self.handle = client().simxGetObjectHandle(name, client().simxServiceCall())

    @staticmethod
    def _relative_to(parent: bool = None, absolute: bool = None, obj_handler: int = None):
        if parent:
            return sim.sim_handle_parent
        elif absolute:
            return -1
        elif obj_handler:
            return obj_handler

        raise ValueError

    def get_orientation(self, *, parent: bool = None, absolute: bool = None, obj_handler: int = None):
        relative_to = self._relative_to(parent, absolute, obj_handler)
        alpha, beta, gamma = client().simxGetObjectOrientation(
            self.handle,
            relative_to,
            client().simxServiceCall(),
        )
        return alpha, beta, gamma

    def set_orientation(
        self,
        orientation: Orientation,
        *,
        parent: bool = None,
        absolute: bool = None,
        obj_handler: int = None,
    ):
        relative_to = self._relative_to(parent, absolute, obj_handler)
        client().simxSetObjectOrientation(
            self.handle,
            relative_to,
            orientation,
            client().simxDefaultPublisher(),
        )
