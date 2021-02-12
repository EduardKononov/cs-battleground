import os
import shutil
from pathlib import Path


def main():
    cwd = Path(os.getcwd())

    cur_dir = Path(__file__).absolute().parent
    for path in [
        path
        for path in cur_dir.glob('*')
        if '__' not in str(path)
    ]:
        shutil.copy(path, cwd / path.name)


if __name__ == '__main__':
    main()
