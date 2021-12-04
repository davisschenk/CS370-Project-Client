import asyncio
import websockets

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS
import json
from datetime import datetime

token = "expVdLCJMNICuhLvycfmQ9OTGrRVs7fo5fglmP2pKcQFQd8e-vpcm_0Q0Bwa64VmrepahFR-wOcej9coM77pbQ=="
org = "lord org"
bucket = "lord"

async def main():
    async with websockets.connect("ws://10.0.0.5:8080/", ping_interval=None) as ws:
        client = InfluxDBClient(url="http://localhost:8086", token=token)
        write_api = client.write_api(write_options=ASYNCHRONOUS)
        buckets = set()

        async for message in ws:
            parsed = json.loads(message)
            time = datetime.utcnow()
            typ = parsed.pop("type")

            point = Point(typ)

            for field_name, field_data in parsed.items():
                for data_name, data_value in field_data.items():
                    point.field(f"{field_name}_{data_name}", data_value)


            point.time(time, WritePrecision.NS)
            write_api.write(bucket, org, point)


asyncio.run(main())
