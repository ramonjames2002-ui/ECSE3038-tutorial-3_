from fastapi import FastAPI, HTTPException

app = FastAPI()

readings = [
    {"name": "front-door", "room": "hall",    "temp": 27.4, "online": True},
    {"name": "hall-lamp",  "room": "hall",    "temp": 26.1, "online": True},
    {"name": "attic",      "room": "attic",   "temp": 31.9, "online": True},
    {"name": "fridge",     "room": "kitchen", "temp": 4.2,  "online": False},
    {"name": "patio",      "room": "outside", "temp": 29.8, "online": True},
]
def average_temp(devices):
    total = 0

    for device in devices:
        total += device["temp"]

    return total / len(devices)

def hottest(devices):
    hottest_device = devices[0]

    for device in devices:
        if device["temp"] > hottest_device["temp"]:
            hottest_device = device

    return hottest_device

print(average_temp(readings))
print(hottest(readings))

@app.get("/devices")
async def get_devices():
    return readings

@app.get("/devices/hottest")
async def get_hottest():
    return hottest(readings)

@app.get("/devices/online")
async def get_online_devices():
    online_devices = []

    for device in readings:
        if device["online"] == True:
            online_devices.append(device)

    return online_devices

@app.get("/devices/{name}")
async def get_device(name: str):
    for device in readings:
        if device["name"] == name:
            return device

    raise HTTPException(
        status_code=404,
        detail="No device called " + name
    )
