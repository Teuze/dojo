#!/usr/bin/python3

"""
Dojo Tactics Server

Usage:
    dojo BOARD PARTY
    markov -h | --help
    markov --version

Options:
    -h --help     Show this screen.
    --version     Show version.
"""

__author__ = "Richard Jarry"
__version__ = "0.1"

import uvicorn

from docopt import docopt
from fastapi import FastAPI

from core.game import Game
from core.event import Event

if __name__ == "__main__":

    args = docopt(__doc__)

    app = FastAPI()

    # TODO: change this to load board+players
    game = Game(args["PARTY"], args["BOARD"])

    @app.get("/players")
    def get_players():
        return game.party

    @app.get("/board")
    def get_board():
        return game.board

    @app.put("/events")
    def put_events(event: Event):
        game = game.update(event)
        return game

    # TODO: load toml defaults
    uvicorn.run(app)
