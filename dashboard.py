import asyncio
import json
import websockets
from datetime import datetime
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.text import Text

async def main():
    console = Console()
    layout = Layout()
    layout.split_row(
        Layout(name="GNSS"),
        Layout(name="IMU"),
        Layout(name="Filter")
    )

    layout["GNSS"].split_column(
        Layout(name="GNSS_llh"),
        Layout(name="GNSS_fi"),
        Layout(name="GNSS_ned")
    )

    layout["IMU"].split_column(
        Layout(name="IMU_accelerometer"),
        Layout(name="IMU_gyroscope"),
        Layout(name="IMU_magnetometer"),
    )

    layout["Filter"].split_column(
        Layout(name="Filter_euler")
    )

    async with websockets.connect("ws://10.0.0.5:8080/", ping_interval=None) as ws:
        with Live(layout, refresh_per_second=10) as live:
            async for message in ws:
                parsed = json.loads(message)

                if parsed.get("type") == "GNSS" and parsed.get("llh"):
                    t = Text()
                    t.append("LLH\n", style="bold green")
                    t.append(f"Latitude: {parsed['llh']['latitude']}\n")
                    t.append(f"Longitude: {parsed['llh']['longitude']}\n")
                    t.append(f"HAE: {parsed['llh']['hae']}\n")
                    t.append(f"MSL: {parsed['llh']['msl']}\n")
                    layout["GNSS_llh"].update(t)
                
                if parsed.get("type") == "GNSS" and parsed.get("fix_information"):
                    t = Text()
                    t.append("Fix Information\n", style="bold green")
                    t.append(f"SVS: {parsed['fix_information']['svs']}\n")
                    t.append(f"Fix Type: {parsed['fix_information']['fix_type']}\n")
                    layout["GNSS_fi"].update(t)
                
                if parsed.get("type") == "GNSS" and parsed.get("ned_velocity"):
                    t = Text()
                    t.append("NED Velocity\n", style="bold green")
                    t.append(f"Speed: {parsed['ned_velocity']['speed']} m/s ({parsed['ned_velocity']['speed'] * 2.237} mph)\n")
                    t.append(f"Ground Speed: {parsed['ned_velocity']['ground_speed']} m/s ({parsed['ned_velocity']['ground_speed'] * 2.237} mph)\n")
                    t.append(f"Heading: {parsed['ned_velocity']['heading']} degrees\n\n")
                    
                    t.append(f"North Velocity: {parsed['ned_velocity']['north']}\n")
                    t.append(f"East Velocity: {parsed['ned_velocity']['east']}\n")
                    t.append(f"Down Velocity: {parsed['ned_velocity']['down']}\n")

                    layout["GNSS_ned"].update(t)

                if parsed.get("type") == "IMU" and parsed.get("accelerometer"):
                    t = Text()
                    t.append("Accelerometer\n", style="bold green")
                    t.append(f"X: {parsed['accelerometer']['x']}\n")
                    t.append(f"Y: {parsed['accelerometer']['y']}\n")
                    t.append(f"Z: {parsed['accelerometer']['z']}\n")
                    layout["IMU_accelerometer"].update(t)



                if parsed.get("type") == "IMU" and parsed.get("gyro"):
                    t = Text()
                    t.append("Gyroscope\n", style="bold green")
                    t.append(f"X: {parsed['gyro']['x']}\n")
                    t.append(f"Y: {parsed['gyro']['y']}\n")
                    t.append(f"Z: {parsed['gyro']['z']}\n")
                    layout["IMU_gyroscope"].update(t)

                if parsed.get("type") == "IMU" and parsed.get("magnetometer"):
                    t = Text()
                    t.append("Magnetometer\n", style="bold green")
                    t.append(f"X: {parsed['magnetometer']['x']}\n")
                    t.append(f"Y: {parsed['magnetometer']['y']}\n")
                    t.append(f"Z: {parsed['magnetometer']['z']}\n")
                    layout["IMU_magnetometer"].update(t)

                if parsed.get("type") == "FILTER" and parsed.get("euler_angles"):
                    t = Text()
                    t.append("Euler Angles\n", style="bold green")
                    t.append(f"Roll: {parsed['euler_angles']['roll']}\n")
                    t.append(f"Pitch: {parsed['euler_angles']['pitch']}\n")
                    t.append(f"Yaw: {parsed['euler_angles']['yaw']}\n")

                    layout["Filter_euler"].update(t)

asyncio.run(main())


