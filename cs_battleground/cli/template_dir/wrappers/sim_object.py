from cs_battleground.robot_objects_tree import RobotObjectsTree

__all__ = ['SimObject']


class SimObject:
    """
    Базовый объект для всех оберток над объектами CoppeliaSim.
    Определяет логику получения хендлера объекта.
    """

    def __init__(self, name: str):
        self.name = name

        self.handle = RobotObjectsTree()[name]
