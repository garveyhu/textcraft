import threading

import uvicorn

from textcraft.api.fast_api import app
from textcraft.api.gradio_web import iface
from textcraft.config import Config

cfg = Config()


def run_uvicorn():
    uvicorn.run(app, host="0.0.0.0", port=8000)


def run_gradio():
    iface.launch()


def main():
    uvicorn_thread = threading.Thread(target=run_uvicorn)
    gradio_thread = threading.Thread(target=run_gradio)

    uvicorn_thread.start()
    gradio_thread.start()

    uvicorn_thread.join()
    gradio_thread.join()


if __name__ == "__main__":
    main()
