from langserve import add_routes

from textcraft.chains.joketeller import get_chain


def langserve_router(app):
    add_routes(app, get_chain(), path="/langserve")
