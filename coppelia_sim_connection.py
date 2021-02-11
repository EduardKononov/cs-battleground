import os
from contextlib import contextmanager

import b0RemoteApi

_CLIENT = None


def client() -> b0RemoteApi.RemoteApiClient:
    global _CLIENT
    if _CLIENT is None:
        raise ValueError('You can use client() only within `coppelia_sim_connection` context')
    return _CLIENT


@contextmanager
def coppelia_sim_connection(ip):
    with b0RemoteApi.RemoteApiClient() as client:
        os.environ['B0_RESOLVER'] = f'tcp://{ip}:22000'
        global _CLIENT
        _CLIENT = client
        yield client
