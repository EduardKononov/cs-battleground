from cs_battleground.remote_api.coppelia_sim_connection import client
from cs_battleground.wrappers.sim_base import SimBase

__all__ = ['Joint']


class Joint(SimBase):
    def __init__(self, joint_name, scaler=1):
        """
        Обертка над объектом joint для упрощения базовых операций

        :param joint_name: имя joint'а (прямо из CoppeliaSim)
        :param scaler: значение, на которое умножается каждое выставляемое velocity
        """
        super(Joint, self).__init__(joint_name)

        self._velocity = client().simxGetJointTargetVelocity(self.handle, client().simxServiceCall())
        self.scaler = scaler

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        new_velocity = self.scaler * velocity

        if self.velocity != new_velocity:
            client().simxSetJointTargetVelocity(self.handle, new_velocity, client().simxDefaultPublisher())
            self._velocity = new_velocity
