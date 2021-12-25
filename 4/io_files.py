from pathlib import Path
from typing import List


def read_passwords(path: Path) -> List[str]:
    with open(path, 'r') as file:
        return [line[:-1] for line in file.readlines()]


def write_passwords(path: Path, data: List[str]):
    with open(path, 'w') as file:
        for p in data:
            file.write(p + '\n')

