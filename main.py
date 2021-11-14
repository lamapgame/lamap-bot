#!/usr/bin/env python3

from fastapi import FastAPI
from helpers import top_players, top_rich_players, top_pauvrards

app = FastAPI()


@app.get("/")
def root():
    return {"API": "Lamap Bot"}


@app.get("/leaderboard")
async def get_top_players():
    top_players_list = top_players()
    top_players_result_list = list()
    for idx, user in enumerate(top_players_list, start=1):
        id = user.id
        name = user.name
        points = user.points
        nkap = user.nkap
        top_players_result_list.append(
            {"position": idx, "id": id, "name": name, "points": points, "nkap": nkap})
    return top_players_result_list


@app.get("/leaderboard-rich")
async def get_top_players():
    top_players_list = top_rich_players()
    top_players_result_list = list()
    for idx, user in enumerate(top_players_list, start=1):
        id = user.id
        name = user.name
        points = user.points
        nkap = user.nkap
        top_players_result_list.append(
            {"position": idx, "id": id, "name": name, "points": points, "nkap": nkap})
    return top_players_result_list


@app.get("/leaderboard-poor")
async def get_top_players():
    top_players_list = top_pauvrards()
    top_players_result_list = list()
    for idx, user in enumerate(top_players_list, start=1):
        id = user.id
        name = user.name
        points = user.points
        nkap = user.nkap
        top_players_result_list.append(
            {"position": idx, "id": id, "name": name, "points": points, "nkap": nkap})
    return top_players_result_list
