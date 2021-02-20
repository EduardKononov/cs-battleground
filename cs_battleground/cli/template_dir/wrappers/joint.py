from cs_battleground.remote_api import (
    sim,
    # ctrl + click по методу, чтобы перейти к исходникам и почитать документацию
    client,
)
from cs_battleground.cli.template_dir.wrappers import SimObject

__all__ = ['Joint']


class Joint(SimObject):
    def __init__(self, joint_name, velocity_scaler=1):
        """
        Обертка над объектом joint для упрощения базовых операций.

        :param joint_name: имя joint'а (прямо из CoppeliaSim)
        :param velocity_scaler: значение, на которое умножается каждое выставляемое velocity
        """
        super(Joint, self).__init__(joint_name)

        self._target_velocity = client().simxGetJointTargetVelocity(self.handle, client().simxServiceCall())
        self._target_position = client().simxGetJointTargetPosition(self.handle, client().simxServiceCall())
        self.velocity_scaler = velocity_scaler

    def _change_motor_state(self, enabled: int):
        client().simxSetObjectIntParameter(
            self.handle,
            sim.sim_jointintparam_motor_enabled,
            enabled,
            client().simxDefaultPublisher(),
        )

    def enable_motor(self):
        self._change_motor_state(1)

    def disable_motor(self):
        self._change_motor_state(0)

    def _change_control_loop_state(self, enabled):
        client().simxSetObjectIntParameter(
            self.handle,
            sim.sim_jointintparam_ctrl_enabled,
            enabled,
            client().simxDefaultPublisher(),
        )

    def enable_control_loop(self):
        self._change_control_loop_state(1)

    def disable_control_loop(self):
        self._change_control_loop_state(0)

    @property
    def target_position(self):
        return self._target_position

    @target_position.setter
    def target_position(self, position):
        if self.target_position != position:
            client().simxSetJointTargetPosition(
                self.handle,
                position,
                client().simxDefaultPublisher()
            )
            self._target_velocity = position

    @property
    def target_velocity(self):
        return self._target_velocity

    @target_velocity.setter
    def target_velocity(self, velocity):
        new_velocity = self.velocity_scaler * velocity

        if self.target_velocity != new_velocity:
            client().simxSetJointTargetVelocity(
                self.handle,
                new_velocity,
                client().simxDefaultPublisher()
            )
            self._target_velocity = new_velocity

    @property
    def target_position(self):
        return self._target_position

    @target_position.setter
    def target_position(self, radian_angle):
        if self.target_position != radian_angle:
            client().simxSetJointTargetPosition(
                self.handle,
                radian_angle,
                client().simxDefaultPublisher(),
            )
            self._target_position = radian_angle
