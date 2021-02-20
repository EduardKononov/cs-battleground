from contextlib import contextmanager

from cs_battleground.remote_api import client

__all__ = ['loaded_robot']


@contextmanager
def loaded_robot(model_path: str):
    with open(model_path, 'rb') as file:
        buffer = file.read()
    handle = client().simxLoadModelFromBuffer(buffer, client().simxServiceCall())

    try:
        yield
    finally:
        client().simxRemoveObjects([handle], 1, client().simxDefaultPublisher())
