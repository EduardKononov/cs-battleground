from cs_battleground.robot_controller import (
    RobotController,
    start_control_session,
)
from cs_battleground.remote_api import coppelia_sim_connection
from cs_battleground.wrappers import Joint


# pioneer.ttt
class PioneerController(RobotController):
    def __init__(self):
        super(PioneerController, self).__init__()
        self.right_joint = Joint('Pioneer_p3dx_rightMotor')
        self.left_joint = Joint('Pioneer_p3dx_leftMotor')

    def forward(self):
        self.left_joint.velocity = 1
        self.right_joint.velocity = 1

    def backward(self):
        self.left_joint.velocity = -1
        self.right_joint.velocity = -1

    def stop(self):
        self.left_joint.velocity = 0
        self.right_joint.velocity = 0

    def turn_right(self):
        self.left_joint.velocity = 1.5
        self.right_joint.velocity = 0.5

    def turn_left(self):
        self.left_joint.velocity = 0.5
        self.right_joint.velocity = 1.5

    def backward_turn_right(self):
        self.left_joint.velocity = -1.5
        self.right_joint.velocity = -0.5

    def backward_turn_left(self):
        self.left_joint.velocity = -0.5
        self.right_joint.velocity = -1.5

    def set_base_velocity(self, value):
        self.left_joint.scaler = value
        self.right_joint.scaler = value


def main():
    with coppelia_sim_connection('localhost'):
        controller = PioneerController()
        start_control_session(
            controller,
            {
                # speedup
                'k': lambda: controller.set_base_velocity(3),
            },
            {
                'k': lambda: controller.set_base_velocity(1),
            },
        )


if __name__ == '__main__':
    main()
