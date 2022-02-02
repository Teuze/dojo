from fastapi import FastAPI

# from pydantic.dataclasses import dataclass

import core.game
import core.board
import core.event
import core.player

app = FastAPI()


@app.get("/board")
def get_board():
    return


@app.get("/players")
def get_players():
    return


@app.put("/action")
def put_action(action: core.event.Action):
    return
