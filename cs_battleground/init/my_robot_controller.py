# Может показаться, что данный файл большой, но на самом деле это совсем не так.
# Разберитесь, как он работает, а потом ЗАПУСТИТЕ ГЕНЕРАЦИЮ ЕЩЕ РАЗ с флагом --no-comments
# python -m cs_battleground.init --no-comments
# ВМЕСТО ЭТОГО ФАЙЛА сгенерируется НОВЫЙ ФАЙЛ БЕЗ КОММЕНТАРИЕВ

from cs_battleground.remote_api import (
    coppelia_sim_connection,
    loaded_robot,
    client,
    # в примере ниже функция client не используется, но она наверняка понадобится
    # если требуется работать с чем-то кроме joit'ов.
    # client -- ваш доступ ко всем возможнотсям Remote API.
    # Полный список можно найти по этой ссылке:
    # https://www.coppeliarobotics.com/helpFiles/en/b0RemoteApi-functionList.htm
    # Находите нужный метод, переходите по Python, смотрите документацию и используете.
    # Пример:
    # client().simxSetJointTargetVelocity(joint_handle, velocity, client().simxServiceCall())

    # На самом деле, с большего все выглядит так же, как в embedded Lua скриптах внутри Coppelia
    # ВАЖНЫЕ моменты:
    # * client работает ТОЛЬКО внутри контектста coppelia_sim_connection (см. def main)
    # * Почти все методы требуют примечательного атрибута topic. Он определяет, каким образом выполнить запрос к API.
    #   За полным пониманием сюда:
    #   https://www.coppeliarobotics.com/helpFiles/en/b0RemoteApiModusOperandi.htm
    #   Скорее всего хватит первых трех:
    #       * simxServiceCall
    #       * simxDefaultPublisher
    #       * simxDefaultSubscriber
    # * (очень) многие методы API возвращают первым параметром bool значение:
    #       True -- запрос прошел и выпонился успешной
    #       False -- что-то пошло не так
    #   Каждый раз проверять его -- утомительное занятие, потому client проверяет его автоматически
    #   (выбрасывается RuntimeError если вернулся False) и УДАЛЯЕТ его из списка возвращаемых значений.
    #   Т.е. если должно было вернуться два значения (флаг успеха и какая-то полезная нагрузка),
    #   как, например, в simxLoadModelFromFile
    #   (https://www.coppeliarobotics.com/helpFiles/en/b0RemoteApi-python.htm#simxLoadModelFromFile)
    #   то вернется только один объект: item2.
)
from cs_battleground.robot_controller import RobotController
from cs_battleground.keyboard_whatcher import KeyHandler
from cs_battleground.wrappers import Joint


class MyRobotController(RobotController):
    """
    RobotController -- базовый класс для всех кастомных контроллеров.
    Контроллер определяет действия робота в ответ на нажатие клавиш клавиатуры
    и запускает сессию управления.
    """

    def __init__(self):
        super(MyRobotController, self).__init__()

        # Получение joint'ов робота; см. документацию класса в исходниках (зажать ctrl и кликнуть по классу)
        self.right_joint = Joint('Pioneer_p3dx_rightMotor')
        self.left_joint = Joint('Pioneer_p3dx_leftMotor')

    # ОБЯЗАТЕЛЬНЫЕ МЕТОДЫ: начало

    def forward(self):
        """Обработчик нажатия W"""
        self.left_joint.velocity = 1
        self.right_joint.velocity = 1

    def backward(self):
        """Обработчик нажатия S"""
        self.left_joint.velocity = -1
        self.right_joint.velocity = -1

    def stop(self):
        """Данный метод должен переводить робота в состояние покоя"""
        self.left_joint.velocity = 0
        self.right_joint.velocity = 0

    def turn_right(self):
        """Обработчик нажатия W+D"""
        # P.S. Все повороты данного двухколесного робота осуществляются
        # за счет выставления разной скорости вращения моторов
        self.left_joint.velocity = 1.5
        self.right_joint.velocity = 0.5

    def turn_left(self):
        """Обработчик нажатия W+A"""
        self.left_joint.velocity = 0.5
        self.right_joint.velocity = 1.5

    def backward_turn_right(self):
        """Обработчик нажатия S+D"""
        self.left_joint.velocity = -1.5
        self.right_joint.velocity = -0.5

    def backward_turn_left(self):
        """Обработчик нажатия S+A"""
        self.left_joint.velocity = -0.5
        self.right_joint.velocity = -1.5

    # ОБЯЗАТЕЛЬНЫЕ МЕТОДЫ: конец
    # После определения перечисленных выше методов,
    # можно определять любое количество других,
    # необходимых именно вашему роботу.

    def set_scaler(self, value):
        self.left_joint.scaler = value
        self.right_joint.scaler = value


def main():
    # Тестирование управления роботом происходит локально, потому на это время вписывать localhost.
    # Во время турнира, вместо localhost нужно написать IP адрес машины, на которой запущена CoppeliaSim
    # со сценой арены
    with coppelia_sim_connection('localhost'):
        # При входе в loaded_robot, на сцену CoppeliaSim будет загружена модель my_robot.
        # Если в модель вшит скрипт, то он запустится как обычно: на старте симуляции
        # При выходе из блока with модель будет АВТОМАТИЧЕСКИ УДАЛЕНА СО СЦЕНЫ
        # P.S. Но только если вы не завершите процесс экстренно с помощью SIGKILL или чего-то подобного.
        #      Если в PyCharm много раз нажать на stop execution, то происходит экстренное завершение.
        #      Чтобы все работало в PyCharm как нужно, включите эмуляцию консоли:
        #      Run -> Edit configurations... -> выбираете нужную конфигурацию -> в секции Execution ставите
        #      галочку на Emulate terminal in output console -> Apply.
        #      Если НЕ ХОТИТЕ ЗАМОРАЧИВАТЬСЯ, то запускайте скрипт через терминал: обычный или в самой IDE
        with loaded_robot('my_robot.ttm'):
            controller = MyRobotController()
            # Описание действия при нажатии клавиши;
            # см. документацию класса в исходниках (зажать ctrl и кликнуть по классу)
            speedup = KeyHandler(
                trigger='k',
                press=lambda: controller.set_scaler(3),
                release=lambda: controller.set_scaler(1),
            )
            # В эту функцию нужно передать дескрипторы всех клавиш, что были определены.
            # Она запустит бесконечный процесс считывания нажатий клавиатуры
            controller.start_control_session([
                speedup,
            ])
            # Для ЗАВЕРШЕНИЕ программы НАЖАТЬ CTRL+C в терминале (НЕ НУЖНО завершать через средства IDE)


if __name__ == '__main__':
    main()
