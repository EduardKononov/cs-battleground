import os
import re
import sys
import shutil
from tempfile import NamedTemporaryFile
from pathlib import Path


def main():
    no_comments = '--no-comments' in sys.argv

    cwd = Path(os.getcwd())

    cur_dir = Path(__file__).absolute().parent
    for path in [
        path
        for path in cur_dir.glob('*')
        if '__' not in str(path)
    ]:
        if path.suffix == '.py' and no_comments:
            with path.open('r') as file:
                text = file.read()
            cleaned = re.sub(r'(.*#.*\n|\n.*""".*""")', '', text).strip() + '\n'

            with NamedTemporaryFile('w+') as file:
                file.write(cleaned)
                file.seek(0)
                temp_path = Path(file.name).absolute()
                shutil.copy(temp_path, cwd / path.name)
            continue

        shutil.copy(path, cwd / path.name)


if __name__ == '__main__':
    main()
