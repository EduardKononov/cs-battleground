import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).absolute().parent.parent))

from cs_battleground.wrappers import Joint
from cs_battleground.remote_api import coppelia_sim_connection, loaded_robot
from cs_battleground.keyboard_whatcher import KeyHandler
from cs_battleground.robot_controller import RobotController


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

    def set_scaler(self, value):
        self.left_joint.scaler = value
        self.right_joint.scaler = value


def main():
    with coppelia_sim_connection('localhost'):
        with loaded_robot('pioneer.ttm'):
            controller = PioneerController()
            speedup = KeyHandler(
                key='k',
                press=lambda: controller.set_scaler(3),
                release=lambda: controller.set_scaler(1),
            )
            controller.start_control_session([
                speedup,
            ])


if __name__ == '__main__':
    main()
