from typing import Union

from fastapi import FastAPI
from bloom.container import UseCases

use_cases = UseCases()

app = FastAPI()

def pos_to_dict(row):
    return {"timestamp": row["timestamp"],
            "speed": row["speed"],
            "course": row["course"],
            "heading": row["heading"],
            "lat": row["lat"],
            "lon": row["lon"]}

@app.get("/vessels")
def get_vessels():
    vessel_repo = use_cases.vessel_repository()
    vessels = vessel_repo.load_all_vessel_metadata()
    resp = []
    for v in vessels:
        resp.append(v)
    return resp

@app.get("/vessels/{mmsi}")
def get_vessels(mmsi: str):
    vessel_repo = use_cases.vessel_repository()
    vessels = vessel_repo.load_vessel_metadata()
    for v in vessels:
        if v.get_mmsi() == int(mmsi):
            return v
    return []


@app.get("/trajectories")
def vessel_trajectories():
    vessel_repo = use_cases.vessel_repository()
    vessels = vessel_repo.load_all_vessel_metadata()
    resp = []
    for v in vessels:
        vt = vessel_repo.get_vessel_trajectory(v.get_mmsi())
        positions = vt.positions
        if not positions.empty:
            resp_positions = positions.apply(pos_to_dict, axis=1)
            resp.append({"mssi":v.get_mmsi(), "positions": list(resp_positions)})
    return resp

@app.get("/trajectories/{mmsi}")
def vessel_trajectories(mmsi: str):
    vessel_repo = use_cases.vessel_repository()
    vt = vessel_repo.get_vessel_trajectory(mmsi)
    positions = vt.positions
    resp_positions = positions.apply(pos_to_dict, axis=1)
    print(len(resp_positions))
    return {"mssi": mmsi, "positions": list(resp_positions)}
