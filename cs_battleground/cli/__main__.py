import os
import re
import shutil
from tempfile import NamedTemporaryFile
from pathlib import Path
from typing import Optional

import typer

from cs_battleground.keyboard_whatcher import KeyboardWatcher

# add_completion=False: https://stackoverflow.com/a/63316503/11179620
TYPER_APP = typer.Typer(add_completion=False)


@TYPER_APP.command('keyboard-test')
def keyboard_test():
    print('Press something')
    with KeyboardWatcher([], verbose=True) as watcher:
        watcher.join()


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
    for path in template_dir.glob('*'):
        if '__' in str(path):
            continue

        if path.suffix == '.py' and no_comments:
            with path.open('r') as file:
                text = file.read()
            cleaned = re.sub(r'(.*#.*\n|\n.*""".*""")', '', text).strip() + '\n'

            with NamedTemporaryFile('w+') as file:
                file.write(cleaned)
                file.seek(0)
                temp_path = Path(file.name).absolute()
                shutil.copy(temp_path, cwd / project_dir / path.name)
            continue

        shutil.copy(path, cwd / project_dir / path.name)

    print(f'New project has been successfully created:\n{project_dir.absolute()}')


def main():
    TYPER_APP()


if __name__ == '__main__':
    main()
