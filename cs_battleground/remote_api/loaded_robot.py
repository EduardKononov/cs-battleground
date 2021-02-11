from contextlib import contextmanager

from cs_battleground.remote_api import client

__all__ = ['loaded_robot']


@contextmanager
def loaded_robot(model_path: str):
    with open(model_path, 'rb') as file:
        buffer = file.read()
    succeed, handle = client().simxLoadModelFromBuffer(buffer, client().simxServiceCall())

    if not succeed:
        raise RuntimeError('Could not load the robot')
    try:
        yield
    finally:
        succeed, _ = client().simxRemoveObjects([handle], 1, client().simxServiceCall())
        print(succeed)
