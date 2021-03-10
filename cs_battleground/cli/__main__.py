import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

import typer

from cs_battleground.keyboard_whatcher import KeyboardWatcher

# add_completion=False: https://stackoverflow.com/a/63316503/11179620
TYPER_APP = typer.Typer(add_completion=False)


@TYPER_APP.command('keyboard-test')
def keyboard_test():
    print('Press something')
    with KeyboardWatcher([], verbose=True) as watcher:
        watcher.join()


@contextmanager
def clean(path, cleaners):
    with path.open('r', encoding='utf-8') as file:
        text = file.read()

    cleaned = text
    for cleaner in cleaners:
        cleaned = cleaner(cleaned)

    class CustomNamedTemporaryFile:
        """
        This custom implementation is needed because of the following limitation of tempfile.NamedTemporaryFile:

        > Whether the name can be used to open the file a second time, while the named temporary file is still open,
        > varies across platforms (it can be so used on Unix; it cannot on Windows NT or later).
        """

        def __init__(self, mode='wb', delete=True):
            self._mode = mode
            self._delete = delete

        def __enter__(self):
            # Generate a random temporary file name
            file_name = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
            # Ensure the file is created
            open(file_name, 'x', encoding='utf-8').close()
            # Open the file in the given mode
            self._tempFile = open(file_name, self._mode, encoding='utf-8')
            return self._tempFile

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._tempFile.close()
            if self._delete:
                os.remove(self._tempFile.name)

    with CustomNamedTemporaryFile('w+') as file:
        file.write(cleaned)
        file.seek(0)
        temp_path = Path(file.name).absolute()
        yield temp_path


@TYPER_APP.command('create-app')
def create_app(
    app_name: str,
    no_comments: Optional[bool] = typer.Option(False, '--no-comments'),
):
    cwd = Path(os.getcwd())
    project_dir = cwd / app_name

    try:
        project_dir.mkdir()
    except FileExistsError:
        print(f'Directory "{app_name}" already exists. Aborted.')
        exit(1)

    template_dir = Path(__file__).absolute().parent / 'template_dir'

    def rec_copy_dir(dir_path: Path, copy_to: Path):
        for path in dir_path.glob('*'):
            if '__pycache__' in str(path):
                continue

            if path.is_dir():
                copy_to = copy_to / path.name
                copy_to.mkdir()
                rec_copy_dir(path, copy_to)
            elif path.is_file():
                if path.suffix == '.py':
                    cleaners = [
                        lambda text: text.replace('cs_battleground.cli.template_dir.', ''),
                    ]

                    if no_comments:
                        cleaners.append(lambda text: re.sub(r'(.*#.*\n|\n.*""".*""")', '', text).strip() + '\n')

                    with clean(path, cleaners) as temp_path:
                        shutil.copy(temp_path, copy_to / path.name)
                else:
                    shutil.copy(path, copy_to / path.name)

    rec_copy_dir(template_dir, project_dir)

    coppelia_dir = Path(__file__).absolute().parent.parent / 'arena_files' / 'coppelia'
    for file in (
        'battleground.ttt',
        'robot.ttm',
    ):
        shutil.copy(coppelia_dir / file, project_dir / file)

    print(f'New project has been successfully created:\n{project_dir.absolute()}')


def main():
    TYPER_APP()


if __name__ == '__main__':
    main()
