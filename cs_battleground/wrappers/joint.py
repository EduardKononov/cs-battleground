from cs_battleground.remote_api.coppelia_sim_connection import client

__all__ = ['Joint']


class Joint:
    def __init__(self, joint_name, scaler=1):
        """
        Обертка над объектом joint для упрощения базовых операций

        :param joint_name: имя joint'а (прямо из CoppeliaSim)
        :param scaler: значение, на которое умножается каждое выставляемое velocity
        """
        joint_handler = client().simxGetObjectHandle(joint_name, client().simxServiceCall())

        self.handler = joint_handler

        self._velocity = client().simxGetJointTargetVelocity(self.handler, client().simxServiceCall())
        self.scaler = scaler

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        new_velocity = self.scaler * velocity

        if self.velocity != new_velocity:
            client().simxSetJointTargetVelocity(self.handler, new_velocity, client().simxDefaultPublisher())
            self._velocity = new_velocity
