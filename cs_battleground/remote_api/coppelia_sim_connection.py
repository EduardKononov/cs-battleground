import os
from contextlib import contextmanager

from cs_battleground.remote_api import b0RemoteApi

_CLIENT = None

__all__ = [
    'client',
    'coppelia_sim_connection',
]


def client() -> b0RemoteApi.RemoteApiClient:
    """
    client -- ваш доступ ко всем возможнотсям Remote API.
    Полный список можно найти по этой ссылке:
    https://www.coppeliarobotics.com/helpFiles/en/b0RemoteApi-functionList.htm
    Находите нужный метод, переходите по Python, смотрите документацию и используете.
    Пример:
    client().simxSetJointTargetVelocity(joint_handle, velocity, client().simxServiceCall())

    На самом деле, с большего все выглядит так же, как в embedded Lua скриптах внутри Coppelia
    ВАЖНЫЕ моменты:
    * client работает ТОЛЬКО внутри контектста coppelia_sim_connection (см. def main)
    * Почти все методы требуют примечательного атрибута topic. Он определяет, каким образом выполнить запрос к API.
      За полным пониманием сюда:
      https://www.coppeliarobotics.com/helpFiles/en/b0RemoteApiModusOperandi.htm
      Скорее всего хватит первых трех:
          * simxServiceCall
          * simxDefaultPublisher
          * simxDefaultSubscriber
    * (очень) многие методы API возвращают первым параметром bool значение:
          True -- запрос прошел и выпонился успешной
          False -- что-то пошло не так
      Каждый раз проверять его -- утомительное занятие, потому client проверяет его автоматически
      (выбрасывается RuntimeError, если вернулся False) и УДАЛЯЕТ его из списка возвращаемых значений.
      Т.е. если должно было вернуться два значения (флаг успеха и какая-то полезная нагрузка),
      как, например, в simxLoadModelFromFile
      (https://www.coppeliarobotics.com/helpFiles/en/b0RemoteApi-python.htm#simxLoadModelFromFile)
      то вернется только один объект: item2.
    """

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

        try:
            yield client
        except (KeyboardInterrupt, SystemExit):
            print('\n\nSIMULATION HAS BEEN STOPPED BY USER\n\n')
            exit(0)
