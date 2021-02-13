import time
from threading import Thread
from functools import partial
from typing import NamedTuple, Callable, Optional, Sequence

from pynput.keyboard import Listener, KeyCode, Key

__all__ = [
    'KeyDescriptor',
    'KeyboardWatcher',
]


def _handle_cycle(key_pool, handlers):
    handled = set()

    name: str
    for name in handlers:
        keys = set(name.split('+'))
        all_pressed = all(
            key in key_pool
            for key in keys
        )
        all_unhandled = not any(
            key in handled
            for key in keys
        )
        if all_pressed and all_unhandled:
            handlers[name]()
            handled |= keys


def infinite_handle_cycle(key_pool, handlers):
    while True:
        time.sleep(0.1)
        _handle_cycle(key_pool, handlers)


class KeyDescriptor(NamedTuple):
    # какую кнопку/комбинацию нужно нажать, чтобы спровоцировать действие
    # Примеры: 'w', 'w+a'
    key: str
    # действие на нажатие кнопки
    press: Optional[Callable] = None
    # действие на отжатие кнопки
    release: Optional[Callable] = None


class KeyboardWatcher:
    def __init__(self, key_handlers: Sequence):
        self._pressed = set()
        self._released = set()

        self._press_handlers = {}
        self._release_handlers = {}

        sorted_key_handlers = sorted(key_handlers, key=lambda x: len(x.key), reverse=True)
        for key, press, release in sorted_key_handlers:
            if press:
                self._press_handlers[key] = press
            if release:
                self._release_handlers[key] = release

        self._listener = None

        target = partial(infinite_handle_cycle, key_pool=self._pressed, handlers=self._press_handlers)
        thread = Thread(target=target, daemon=True)
        thread.start()

    @staticmethod
    def _get_pressed_key(key: KeyCode):
        if isinstance(key, KeyCode):
            key_name = key.char
        elif isinstance(key, Key):
            key_name = key.name
        else:
            raise ValueError

        try:
            key_name = key_name.lower()
        except AttributeError:
            return None

        return key_name

    def handle_press(self, key: KeyCode):
        key_name = self._get_pressed_key(key)

        if key_name:
            self._pressed.add(key_name)

    def handle_release(self, key: KeyCode):
        key_name = self._get_pressed_key(key)

        if key_name in self._pressed:
            self._pressed.remove(key_name)
            self._released.add(key_name)

            _handle_cycle(self._released, self._release_handlers)
            self._released.remove(key_name)

    def join(self):
        self._listener.join()

    def __enter__(self):
        self._listener = Listener(
            on_press=self.handle_press,
            on_release=self.handle_release,
            # suppress=True,
        )
        self._listener.start()
        self._listener.wait()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._listener.stop()


def main():
    wd = KeyDescriptor(
        key='w+d',
        press=lambda: print('pressed w+d'),
        release=lambda: print('released w+d'),
    )
    w = KeyDescriptor(
        key='w',
        press=lambda: print('pressed w'),
        release=lambda: print('released w'),
    )
    with KeyboardWatcher([wd, w]) as handler:
        handler.join()


if __name__ == '__main__':
    main()
