import os
import sys


def main():
    try:
        import poetry.factory
    except ModuleNotFoundError:
        os.system(
            f"{sys.executable} -m pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple"
        )


if __name__ == "__main__":
    main()
