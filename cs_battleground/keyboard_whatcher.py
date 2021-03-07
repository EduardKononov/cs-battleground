import time
from threading import Thread, Lock
from functools import partial
from contextlib import suppress
from typing import NamedTuple, Callable, Optional, Sequence, Dict
from dataclasses import dataclass

from pynput.keyboard import Listener, KeyCode, Key

__all__ = [
    'KeyHandler',
    'KeyboardWatcher',
]


class SafeSet(set):
    def __init__(self, name, *args):
        super(SafeSet, self).__init__(*args)
        self.lock = Lock()
        self.name = name

    def add(self, element) -> None:
        with self.lock:
            super(SafeSet, self).add(element)
        # if self.name == 'pressed':
        #     print(f'[{self.name}] add {element} {self}')

    def remove(self, element) -> None:
        with self.lock:
            super(SafeSet, self).remove(element)
        # if self.name == 'pressed':
        #     print(f'[{self.name}] remove {element} {self}')

    def __str__(self):
        return '+'.join(self)


@dataclass
class KeyHandler:
    # какую кнопку/комбинацию нужно нажать, чтобы спровоцировать действие
    # Примеры: 'w', 'w+a'
    trigger: str
    # действие на нажатие кнопки
    press: Optional[Callable] = None
    # действие на отжатие кнопки
    release: Optional[Callable] = None

    def __post_init__(self):
        self.keys = set(self.trigger.split('+'))


class KeyPool(NamedTuple):
    pressed = SafeSet('pressed')
    released = SafeSet('released')


def _handle_cycle(
    active_keys: set,
    handlers: Dict[str, KeyHandler],
    handle_method_name: str,
):
    handled = set()

    name: str
    for handler in handlers.values():
        keys = handler.keys
        triggered = all(
            key in active_keys
            for key in keys
        )

        all_unhandled = not any(
            key in handled
            for key in keys
        )

        if triggered and all_unhandled:
            with suppress(TypeError):
                getattr(handler, handle_method_name)()

            handled |= keys


def infinite_handle_cycle(*args, **kwargs):
    while True:
        time.sleep(0.05)
        _handle_cycle(*args, **kwargs)


class KeyboardWatcher:
    def __init__(self, key_handlers: Sequence, verbose: bool = False):
        self._pool = KeyPool()
        self._verbose = verbose

        # sort them in order to give combinations precedence
        key_handlers = sorted(
            key_handlers,
            key=lambda x: len(x.trigger),
            reverse=True,
        )
        self._handlers = {
            handler.trigger: handler
            for handler in key_handlers
        }

        self._listener = None

        target = partial(
            infinite_handle_cycle,
            active_keys=self.pressed,
            handlers=self._handlers,
            handle_method_name='press'
        )
        hold_thread = Thread(target=target, daemon=True)
        hold_thread.start()

        self._listener = Listener(
            on_press=self.handle_press,
            on_release=self.handle_release,
            # suppress=True,
        )

    @property
    def pressed(self):
        return self._pool.pressed

    @property
    def released(self):
        return self._pool.released

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

        if (
            key_name and
            key_name not in self.pressed
        ):
            self.pressed.add(key_name)

        if self._verbose:
            print(f'pressed: {self.pressed}')

    def handle_release(self, key: KeyCode):
        key_name = self._get_pressed_key(key)

        if key_name in self.pressed:
            self.pressed.remove(key_name)
            self.released.add(key_name)

            _handle_cycle(self.released, self._handlers, 'release')
            self.released.remove(key_name)

        if self._verbose:
            print(f'released: {self.pressed}')

    def join(self):
        while self._listener.is_alive():
            self._listener.join(0.1)

    def __enter__(self):
        self._listener.start()
        self._listener.wait()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._listener.stop()

    def start(self):
        self._listener.start()
        while True:
            time.sleep(0.1)


def main():
    def dummy(trigger):
        return KeyHandler(
            trigger=trigger,
            press=lambda: print(f'pressed {trigger}'),
            release=lambda: print(f'released {trigger}'),
        )

    watcher = KeyboardWatcher([
        dummy('w+d'),
        dummy('d'),
        dummy('k'),
        dummy('w'),
    ])
    try:
        watcher.start()
    finally:
        print('finally')


if __name__ == '__main__':
    main()
