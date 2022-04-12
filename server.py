#!/usr/bin/python3

"""
Dojo Tactics Server

Usage:
    server <board> <players>
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

import secrets

from docopt import docopt

from fastapi import FastAPI
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials

from core.board import Board
from core.player import Player
from core.action import *
from core.event import Event
from core.game import Game

if __name__ == "__main__":

    args = docopt(__doc__, version=__version__)
    
    path = args["<players>"]
    files = os.listdir(path)

    players = [Player.parse_file(path+f) for f in files]

    board = Board.parse_file(args["<board>"])

    game = Game(board=board, players=players, events=[], states=[])

    # Prepare auth token for each player (names should be unique)
    tokens = {p.name: secrets.token_hex(12) for p in players}

    app = FastAPI()
    sec = HTTPBasic()
    print(tokens)

    def auth(credentials: HTTPBasicCredentials = Depends(sec)):
        # Pre-fetch password to even out lookup times
        if credentials.username in tokens.keys():
            password = tokens[credentials.username]
        else:
            password = None

        c1 = credentials.username in tokens.keys()
        c2 = secrets.compare_digest(credentials.password, password)

        if c1 and c2:
            return credentials.username

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect player name or password",
            headers={"WWW-Authenticate": "Basic"}
        )

    @app.get("/")
    def get_root():
        return game

    @app.get("/turn")
    def get_board():
        return game.turn

    @app.get("/board")
    def get_board():
        return game.board

    @app.get("/players")
    def get_players():
        return game.players

    @app.get("/events")
    def get_events():
        return game.events

    @app.post("/play")
    def post_event(action_name: str, x: int, y: int, player_name=Depends(auth)):
        valid_actions = {a.__name__: a() for a in Action.__subclasses__()}
        valid_players = {p.name: p for p in game.players}

        action = valid_actions[action_name]
        player = valid_players[player_name]

        event = Event(action=action, player=player, target=(x, y))
        
        game.update(event)
        return game

    # TODO: load toml defaults
    # board default: assets/maps/map.json
    # players default: assets/entities/*
    
    uvicorn.run(app)
