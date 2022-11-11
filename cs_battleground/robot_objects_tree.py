from cs_battleground.remote_api import client
from cs_battleground.remote_api.official_coppellia_lib import sim


class _SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# we made it singleton because the program can be used
# for controlling only one model at a time
class RobotObjectsTree(metaclass=_SingletonMeta):
    def __init__(self, robot_base_handle: int = None):
        assert robot_base_handle is not None

        c = client()
        handles = c.simxGetObjectsInTree(
            robot_base_handle,
            sim.sim_handle_all,
            # include base
            0,
            c.simxServiceCall(),
        )
        self.objects = {
            c.simxGetObjectName(handle, False, c.simxServiceCall()).decode('utf-8'): handle
            for handle in handles
        }

    def __getitem__(self, object_name: str):
        try:
            return self.objects[object_name]
        except KeyError:
            # if you load models which have shapes with identical names
            # the one that is loaded second will be renamed as "name0"
            for name, obj in self.objects.items():
                name = name[:-1]
                if name == object_name:
                    return obj

            raise
