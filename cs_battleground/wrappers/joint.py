from cs_battleground.remote_api.coppelia_sim_connection import client

__all__ = ['Joint']


class Joint:
    def __init__(self, joint_name, base_velocity=1):
        succeed, joint_handler = client().simxGetObjectHandle(joint_name, client().simxServiceCall())
        if not succeed:
            raise RuntimeError('Could not get object handle')
        self.handler = joint_handler

        self._velocity = None
        self.scaler = base_velocity

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        new_velocity = self.scaler * velocity

        if self.velocity != new_velocity:
            client().simxSetJointTargetVelocity(self.handler, new_velocity, client().simxDefaultPublisher())
            self._velocity = new_velocity
