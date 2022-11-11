from typing import Union

# ВАЖНАЯ ФУНКЦИЯ! см. документацию
from cs_battleground.remote_api import client
# Модуль sim предоставляется самой коппелией. Макароны внутри -- не мое.
# Содержит различные константы, которые могут потребовать при работе с API
from cs_battleground.remote_api.official_coppellia_lib import sim
from cs_battleground.cli.template_dir.wrappers import SimObject

__all__ = ['Joint']


class Joint(SimObject):
    def __init__(self, joint_name: str):
        """
        Обертка над объектом joint для упрощения базовых операций.

        :param joint_name: имя joint'а (прямо из CoppeliaSim)
        """
        super(Joint, self).__init__(joint_name)

        self._target_velocity = client().simxGetJointTargetVelocity(self.handle, client().simxServiceCall())
        self._target_position = client().simxGetJointTargetPosition(self.handle, client().simxServiceCall())

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

    def _change_control_loop_state(self, enabled: int):
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
    def target_position(self, position: Union[int, float]):
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
    def target_velocity(self, velocity: Union[int, float]):

        if self.target_velocity != velocity:
            client().simxSetJointTargetVelocity(
                self.handle,
                velocity,
                client().simxDefaultPublisher()
            )
            self._target_velocity = velocity

    @property
    def target_position(self):
        return self._target_position

    @target_position.setter
    def target_position(self, radian_angle: Union[int, float]):
        if self.target_position != radian_angle:
            client().simxSetJointTargetPosition(
                self.handle,
                radian_angle,
                client().simxDefaultPublisher(),
            )
            self._target_position = radian_angle
