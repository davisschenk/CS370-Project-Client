import asyncio
import websockets
from aioinflux import InfluxDBClient
import json

async def main():
    async with websockets.connect("ws://127.0.0.1:8080/") as ws, InfluxDBClient(db="db0") as idb:
        async for message in ws:
            parsed = json.loads(message)

            if parsed.get("type") == "IMU":
                print(parsed.get("accelerometer"))


asyncio.run(main())
