import random
import datetime
from fastapi import FastAPI

app = FastAPI()

# Initial temperature state
station_temperatures = {}

# Predefined list of weather stations
stations = [
    {"id": 1, "name": "Station Alpha"},
    {"id": 2, "name": "Station Beta"},
    {"id": 3, "name": "Station Gamma"}
]

def generate_temperatures(station_id):
    now = datetime.datetime.utcnow()
    if station_id not in station_temperatures:
        station_temperatures[station_id] = [(now, 20.0)]

    last_timestamp, last_temp = station_temperatures[station_id][-1]
    while last_timestamp + datetime.timedelta(minutes=5) <= now:
        last_timestamp += datetime.timedelta(minutes=5)
        last_temp += round(random.uniform(-0.2, 0.2), 2)
        station_temperatures[station_id].append((last_timestamp, round(last_temp, 2)))

    return station_temperatures[station_id]

@app.get("/status")
def status():
    return {}

@app.get("/station/list")
def list_stations():
    return {"stations": stations}

@app.get("/station/{station_id}/temperature")
def last_temperature(station_id: int):
    temperatures = generate_temperatures(station_id)
    timestamp, temp = temperatures[-1]
    return {"timestamp": timestamp.isoformat(), "temperature": temp}

@app.get("/station/{station_id}/temperature/last24hours")
def temperature_last_24_hours(station_id: int):
    temperatures = generate_temperatures(station_id)
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
    last_24h_temps = [(t, temp) for t, temp in temperatures if t >= cutoff]
    return {"temperatures": [{"timestamp": t.isoformat(), "temperature": temp} for t, temp in last_24h_temps]}
