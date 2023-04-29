import asyncio
import json
import os
import websockets
import bpy


async def play_animation(websocket, path):
    bpy.ops.screen.animation_play()
    await websocket.send("Playing animation")


async def pause_animation(websocket, path):
    bpy.ops.screen.animation_cancel()
    await websocket.send("Paused animation")


async def send_materials_list(websocket, path):
    materials = bpy.data.materials

    response = {"type": "materials_list", "data": []}
    for material in materials:
        response["data"].append(material.name)

    await websocket.send(json.dumps(response))


async def send_led_strips_list(websocket, path):
    devices = bpy.context.scene.arduino_devices

    response = {"type": "led_strips_list", "data": []}
    for device in devices:
        for led_strip in device.led_strips:
            material_name = led_strip.material.name if led_strip.material else "None"
            response["data"].append(
                {
                    "device_ip": device.ip_address,
                    "device_port": device.port,
                    "led_strip_index": led_strip.index,
                    "material_name": material_name,
                }
            )

    await websocket.send(json.dumps(response))


async def assign_material(websocket, path):
    data = await websocket.recv()
    data = json.loads(data)

    material_name = data["material_name"]
    led_strip_index = int(data["led_strip_index"])
    device_index = int(data["device_index"])

    material = bpy.data.materials.get(material_name)
    device = bpy.context.scene.arduino_devices[device_index]
    led_strip = device.led_strips[led_strip_index]
    led_strip.material = material

    await websocket.send("Material assigned")


async def handler(websocket, path):
    while True:
        try:
            request = await websocket.recv()
            if request == "play":
                await play_animation(websocket, path)
            elif request == "pause":
                await pause_animation(websocket, path)
            elif request == "materials":
                await send_materials_list(websocket, path)
            elif request == "led_strips":
                await send_led_strips_list(websocket, path)
            elif request.startswith("assign_material"):
                await assign_material(websocket, path)
        except websockets.exceptions.ConnectionClosed:
            break


def start_websocket_server():
    start_server = websockets.serve(handler, "localhost", 8080)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    start_websocket_server()