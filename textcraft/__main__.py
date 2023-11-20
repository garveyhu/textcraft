import subprocess
import threading

import uvicorn

from textcraft.api.main import app


def run_uvicorn():
    uvicorn.run(app, host="0.0.0.0", port=8000)


def run_streamlit():
    subprocess.run(["streamlit", "run", "textcraft/ui/streamlit_ui/Chatbot.py"])


def load_thread(app_function):
    thread = threading.Thread(target=app_function)
    thread.start()
    return thread


def main(apps):
    threads = [load_thread(app) for app in apps]

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    apps = [run_uvicorn]
    main(apps)
