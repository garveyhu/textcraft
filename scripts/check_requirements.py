import os
import sys


def main():
    try:
        import poetry.factory
    except ModuleNotFoundError:
        os.system(f"{sys.executable} -m pip install poetry")


if __name__ == "__main__":
    main()
