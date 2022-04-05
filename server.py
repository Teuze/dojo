#!/usr/bin/python3

"""
Dojo Tactics Server

Usage:
    server <board> <party>
    server -h | --help
    server --version

Options:
    -h --help     Show this screen.
    --version     Show version.
"""

__author__ = "Richard Jarry"
__version__ = "0.1"

import uvicorn
import os

from docopt import docopt
from fastapi import FastAPI

# from core.cell import Cell
from core.board import Board

from core.player import Player
from core.party import Party

# from core.action import Action
from core.event import Event
from core.game import Game

if __name__ == "__main__":

    args = docopt(__doc__, version=__version__)

    app = FastAPI()
    
    path = args["<party>"]
    files = os.listdir(path)
    players = [Player.parse_file(path+f) for f in files]
    party = Party(members=players)

    board = Board.parse_file(args["<board>"])

    game = Game(board=board, party=party, events=[], states=[])

    # TODO: Implement authenticated access to endpoints

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
    # board default: assets/maps/map.json
    # party default: assets/entities/*
    
    uvicorn.run(app)
