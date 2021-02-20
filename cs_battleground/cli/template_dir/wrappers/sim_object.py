from cs_battleground.remote_api import client

__all__ = ['SimObject']


class SimObject:
    def __init__(self, name: str):
        self.name = name
        self.handle = client().simxGetObjectHandle(name, client().simxServiceCall())
