from math import pi, atan

from cs_battleground.remote_api import (
    coppelia_sim_connection,
    loaded_robot,
)
from cs_battleground.robot_controller import start_control_session
from cs_battleground.keyboard_whatcher import KeyHandler

from cs_battleground.cli.template_dir.wrappers import Joint


def calc_rot_angle(leg_1: float, leg_2: float):
    """
    Вычисление угла между гипотенузой и катетом_1.
    Используется для вычисления правильного угла поворота передних колес.

    :param leg_1: катет 1
    :param leg_2: катет 2
    :return:
    """
    return pi - atan(leg_1 / leg_2) - pi / 2


class MyRobotController:
    def __init__(
        self,
        length: float,
        width: float,
        rot_radius: float,
        move_joint_target_velocity: float,
        attack_joint_target_velocity: float,
    ):
        """
        :param length: длина машины (от центра заднего до центра переднего колеса)
        :param width: ширина машины (от центра правого до центра левого колеса)
        :param rot_radius: радиус поворота машины в метрах
        :param move_joint_target_velocity: скорость езды
        :param attack_joint_target_velocity: скорость выбрасывания ядер
        """
        super(MyRobotController, self).__init__()

        self.length = length
        self.width = width
        self.rot_radius = rot_radius

        # джоинты, двигающие робота вперед/назад
        # bl -- backward left
        # br -- backward right
        self.bl_joint = Joint('bl_joint')
        self.br_joint = Joint('br_joint')

        # джоинты для поворота передних колес
        # l -- left
        # r -- right
        self.rot_l_joint = Joint('rot_l_joint')
        self.rot_r_joint = Joint('rot_r_joint')
        for joint in (
            self.rot_l_joint,
            self.rot_r_joint,
        ):
            joint.enable_motor()
            joint.enable_control_loop()
        self.reset_wheels_rotation()

        # робот имеет 4 снаряда, которые выбрасываются и
        # возвращаются на место с помощью призматических джоинтов
        # f, r, l, b -- front, right, left, back
        self.f_prism_joint = Joint('f_prism_joint')
        self.r_prism_joint = Joint('r_prism_joint')
        self.l_prism_joint = Joint('l_prism_joint')
        self.b_prism_joint = Joint('b_prism_joint')

        for joint in (
            self.f_prism_joint,
            self.r_prism_joint,
            self.l_prism_joint,
            self.b_prism_joint,
        ):
            joint.target_velocity = attack_joint_target_velocity
            joint.enable_motor()
            joint.enable_control_loop()
            joint.target_position = 0

        self.move_joint_target_velocity = move_joint_target_velocity

    def move_forward(self):
        self.bl_joint.target_velocity = self.move_joint_target_velocity
        self.br_joint.target_velocity = self.move_joint_target_velocity

    def move_backward(self):
        self.bl_joint.target_velocity = -self.move_joint_target_velocity
        self.br_joint.target_velocity = -self.move_joint_target_velocity

    def stop(self):
        self.br_joint.target_velocity = 0
        self.bl_joint.target_velocity = 0

    def turn_right(self):
        self.rot_l_joint.target_position = -calc_rot_angle(
            self.rot_radius + self.width,
            self.length,
        )
        self.rot_r_joint.target_position = -calc_rot_angle(
            self.rot_radius,
            self.length,
        )

    def turn_left(self):
        self.rot_r_joint.target_position = calc_rot_angle(
            self.rot_radius + self.width,
            self.length,
        )
        self.rot_l_joint.target_position = calc_rot_angle(
            self.rot_radius,
            self.length,
        )

    def reset_wheels_rotation(self):
        self.rot_r_joint.target_position = 0
        self.rot_l_joint.target_position = 0


def main():
    # Во время локального тестирование управления роботом вписывать localhost.
    # Во время турнира, вместо localhost вписать IP адрес машины, на которой запущена CoppeliaSim
    # со сценой арены.
    # Сцену нужно ЗАПУСТИТЬ ПЕРЕД ПОПЫТКОЙ ПОДКЛЮЧИТЬСЯ
    # Если все же хочется иметь возможность подключиться к сцене до запуска, передайте в coppelia_sim_connection
    # `allow_non_started=True` в качестве аргумента.
    with coppelia_sim_connection('localhost', allow_non_started=True):
        # При входе в loaded_robot, на сцену CoppeliaSim будет загружена модель my_robot.
        # Если в модель вшит скрипт, то он запустится как обычно: на старте симуляции
        # При выходе из блока with модель будет АВТОМАТИЧЕСКИ УДАЛЕНА СО СЦЕНЫ
        # P.S. К сожалению, автомтическое удаление работает не всегда, из-за двух причин:
        # * при попытке остановить программу, одна из зависимостей Remote API коппелии может выбросить исключение
        #   и выполнение завершится экстренно, без очистки
        # * существует проблемы с многопоточностью и обработкой сигналов от операционной системы
        #   (нажатия клавиш считываются в отдельном потоке)
        #   Т.е. иногда все же придется удалять модель со сцены самостоятельно.
        #   Но! Поскольку по умолчанию можно подключиться к сцене можно только тогда, когда симуляция запущена,
        #   все загруженные модели будут удалены со сцены, когда симуляции остановится.
        #   Т.е. для очистки хватит перезапуска сцены
        with loaded_robot('robot.ttm'):
            controller = MyRobotController(
                length=0.868005 / 2,
                width=0.693387 / 2,
                rot_radius=0.4,
                move_joint_target_velocity=90,
                attack_joint_target_velocity=5.,
            )
            # start_control_session запускает бесконечный процесс управления роботом.
            # В качестве аргументов принимает хендлеры клавиш.
            # Параметры хэндлера определяют:
            # * клавишу/комбинацию ('w', 'w+a' и т.д.)
            #
            #       ! Если комбинация не работает, возможно, она передана в KeyHandler в неправильном виде.
            #       Выполните `cs-battleground keyboard-test` в терминале и нажмите нужную комбинацию.
            #       На экран будет выведено ее правильное строковое представление.
            #       Скопируйте и вставьте его в соответствующий KeyHandler.
            #       ! Как минимум на линуксе shift обрабатывается неправльно. Не используйте его.
            #       Надежней всего использовать только клавиши с буквами и цифрами; их должно с головой хватить
            #       для реализации управления роботом
            #
            # * действие на нажатие (press)
            # * дейстие на отжатие (release)
            start_control_session([
                KeyHandler('w', press=controller.move_forward, release=controller.stop),
                KeyHandler('a', press=controller.turn_left, release=controller.reset_wheels_rotation),
                KeyHandler('s', press=controller.move_backward, release=controller.stop),
                KeyHandler('d', press=controller.turn_right, release=controller.reset_wheels_rotation),
                # атака (клавиши расположены по аналогии с wasd)
                KeyHandler(
                    trigger='i',
                    press=controller.f_prism_joint.disable_control_loop,
                    release=controller.f_prism_joint.enable_control_loop,
                ),
                KeyHandler(
                    trigger='l',
                    press=controller.r_prism_joint.disable_control_loop,
                    release=controller.r_prism_joint.enable_control_loop,
                ),
                KeyHandler(
                    trigger='j',
                    press=controller.l_prism_joint.disable_control_loop,
                    release=controller.l_prism_joint.enable_control_loop,
                ),
                KeyHandler(
                    trigger='k',
                    press=controller.b_prism_joint.disable_control_loop,
                    release=controller.b_prism_joint.enable_control_loop,
                ),
            ])


if __name__ == '__main__':
    main()
