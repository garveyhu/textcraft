import subprocess
import sys

def install_poetry_and_add_source():
    try:
        import poetry
    except ModuleNotFoundError:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "poetry",
            "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"
        ], check=True)

    # Add the source with the priority set to "default"
    subprocess.run([
        "poetry", "source", "add", "--priority=default", "mirrors", "https://pypi.tuna.tsinghua.edu.cn/simple/"
    ], check=True)

if __name__ == "__main__":
    install_poetry_and_add_source()
