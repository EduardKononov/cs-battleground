from cs_battleground.remote_api import client

__all__ = ['SimObject']


class SimObject:
    """
    Базовый объект для всех оберток над объектами CoppeliaSim.
    Определяет логику получения хендлера объекта.
    """
    def __init__(self, name: str):
        self.name = name
        self.handle = client().simxGetObjectHandle(name, client().simxServiceCall())
