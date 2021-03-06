import json

from contextlib import contextmanager

from cs_battleground.remote_api import client, sim
from cs_battleground.robot_objects_tree import RobotObjectsTree

__all__ = ['loaded_robot']


class Position:
    def __init__(self, pos_dummy_name: str):
        c = client()
        self.obj_name = pos_dummy_name
        self.handle = c.simxGetObjectHandle(pos_dummy_name, c.simxServiceCall())

    @property
    def children(self):
        c = client()
        handles = c.simxGetObjectsInTree(
            self.handle,
            sim.sim_handle_all,
            # do not include base itself
            1,
            c.simxServiceCall(),
        )
        return {
            c.simxGetObjectName(handle, False, c.simxServiceCall()).decode('utf-8'): handle
            for handle in handles
        }

    @property
    def busy(self):
        for name in self.children:
            if 'robot_' in name:
                return True

        return False


class Robot:
    def __init__(self, model_path: str):
        with open(model_path, 'rb') as file:
            buffer = file.read()
        self.handle = client().simxLoadModelFromBuffer(buffer, client().simxServiceCall())

        self.shapes = client().simxGetObjectsInTree(
            self.handle,
            sim.sim_object_shape_type,
            0,
            client().simxServiceCall(),
        )

        # init objects tree
        RobotObjectsTree(self.handle)

    def move_to_start_position(self, position: Position):
        c = client()
        c.simxCallScriptFunction(
            f'move_to_start_position@positions',
            sim.sim_scripttype_customizationscript,
            [self.handle, position.obj_name],
            c.simxServiceCall(),
        )

    def name(self, name):
        while True:
            i = 0
            try:
                client().simxSetObjectName(self.handle, f'robot_{name}')
                break
            except RuntimeError:
                name += f'#{i}'
                i += 1
                if i > 10:
                    raise

    name = property(None, name)

    def parent(self, parent_handle):
        client().simxSetObjectParent(
            self.handle,
            parent_handle,
            True,
            False,
            client().simxServiceCall(),
        )

    parent = property(None, parent)

    def copy_object_orientation(self, object_handle):
        c = client()
        obj_orientation = c.simxGetObjectOrientation(object_handle, -1, c.simxServiceCall())
        c.simxSetObjectOrientation(self.handle, -1, obj_orientation, c.simxServiceCall())

    @property
    def mass(self):
        c = client()
        return sum(
            c.simxExecuteScriptString(f'sim.getShapeMassAndInertia({shape})', c.simxServiceCall())
            for shape in self.shapes
        )

    @property
    def length(self):
        return client().simxGetModelLength(self.handle, client().simxServiceCall())

    @property
    def width(self):
        return client().simxGetModelWidth(self.handle, client().simxServiceCall())

    @property
    def height(self):
        return client().simxGetModelHeight(self.handle, client().simxServiceCall())

    def check_size(self):
        proper_bbox_size = client().simxCallScriptFunction(
            'checkSize@restrictions_funcs',
            sim.sim_scripttype_customizationscript,
            [self.length, self.width, self.height],
            client().simxServiceCall(),
        )

        if not proper_bbox_size:
            limits = client().simxCallScriptFunction(
                'getSizeLimits@restrictions_funcs',
                sim.sim_scripttype_customizationscript,
                [],
                client().simxServiceCall(),
            )

            raise ValueError(
                '?????????? ???? ???????????? ???????????????? ????????????????.\n'
                f'???????????? ????????????: {{\n'
                f'\tlength: {self.length}, \n'
                f'\twidth: {self.width}, \n'
                f'\theight: {self.height}\n'
                f'}}\n'
                f'?????????????? ??????????????: {json.dumps(limits, indent=4)}'
            )

    def check_mass(self):
        mass = self.mass
        min_, max_ = client().simxCallScriptFunction(
            'getMassLimit@restrictions_funcs',
            sim.sim_scripttype_customizationscript,
            [],
            client().simxServiceCall(),
        )
        if mass < min_ or mass > max_:
            raise ValueError(
                f'?????????? ???? ???????????? ???????????????? ?????????? (??????????: {mass}, ??????????????: [{min_}, {max_}])'
            )


@contextmanager
def loaded_robot(
    model_path: str,
    robot_name: str,
    team_name: str,
    ignore_restrictions: bool = False,
):
    c = client()

    positions = (
        Position('player_1_pos'),
        Position('player_2_pos'),
    )

    for position in positions:
        if not position.busy:
            target_position = position
            break
    else:
        raise RuntimeError('No available positions')

    robot = Robot(model_path)

    try:
        if not ignore_restrictions:
            robot.check_size()
            robot.check_mass()

        robot.move_to_start_position(target_position)
        robot.name = robot_name
        robot.parent = target_position.handle

        yield
    finally:
        c.simxRemoveObjects([robot.handle], 1, c.simxDefaultPublisher())
