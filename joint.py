from coppelia_sim_connection import client


class Joint:
    def __init__(self, joint_name, base_velocity=1):
        _, joint_handler = client().simxGetObjectHandle(joint_name, client().simxServiceCall())
        self.handler = joint_handler

        self._velocity = None
        self.base_velocity = base_velocity

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        new_velocity = self.base_velocity * velocity
        if self.velocity != new_velocity:
            client().simxSetJointTargetVelocity(self.handler, new_velocity, client().simxDefaultPublisher())
            self._velocity = new_velocity
