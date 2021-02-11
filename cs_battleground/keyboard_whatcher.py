import time
from threading import Thread
from functools import partial

from pynput.keyboard import Listener, KeyCode


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


class KeyboardWatcher:
    def __init__(self, press_handlers: dict, release_handlers: dict):
        self._pressed = set()
        self._released = set()

        self._press_handlers = press_handlers
        self._release_handlers = release_handlers

        self._listener = None

        target = partial(infinite_handle_cycle, key_pool=self._pressed, handlers=press_handlers)
        thread = Thread(target=target, daemon=True)
        thread.start()

    def handle_press(self, key: KeyCode):
        try:
            char = key.char
        except AttributeError:
            pass
        else:
            if char:
                self._pressed.add(char)

    def handle_release(self, key: KeyCode):
        try:
            char = key.char
        except AttributeError:
            pass
        else:
            if char:
                self._pressed.remove(char)
                self._released.add(char)

                _handle_cycle(self._released, self._release_handlers)
                self._released.remove(char)

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
    with KeyboardWatcher(
        {
            'w+d': lambda: print('pressed w+d'),
            'w': lambda: print('pressed w!'),
        },
        {
            'w': lambda: print('r w'),
            'd': lambda: print('r d'),
        },
    ) as handler:
        handler.join()


if __name__ == '__main__':
    main()
