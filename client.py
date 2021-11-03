import asyncio
import websockets

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS
import json
from datetime import datetime

token = "pB8yB-uXrLI7DsgTuhpV1PG33aaVeyzsOjbKJdA5v-UybePGjLmNMEx4wBsR8KileAK0NEy-7TgkUiCqK3YgMg=="
org = "lord"

async def main():
    async with websockets.connect("ws://127.0.0.1:8080/", ping_interval=None) as ws:
        client = InfluxDBClient(url="http://localhost:8086", token=token)
        write_api = client.write_api(write_options=ASYNCHRONOUS)
        buckets = set()

        async for message in ws:
            parsed = json.loads(message)
            time = datetime.utcnow()
            typ = parsed.pop("type")
            bucket = f"{typ.upper()} Data"

            for field_name, field_data in parsed.items():
                point_name = f"{typ.lower()}_{field_name}"
                
                point = Point(point_name)
                for data_name, data_value in field_data.items():
                    point.field(data_name, data_value)

                point.time(time, WritePrecision.NS)

                write_api.write(bucket, org, point)


asyncio.run(main())
