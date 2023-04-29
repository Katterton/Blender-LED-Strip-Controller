import bpy
from .led_strip import LedStrip
from .arduino_device import ArduinoDevice
from .operators import (AddArduinoDeviceOperator, RemoveArduinoDeviceOperator, AddLedStripMaterialOperator,
                        RemoveLedStripOperator, AddLedStripOperator, StartStopOperator, GenerateArduinoCodeOperator)
from .panels import ArduinoDevicePanel
from .utils import assign_operator_properties



bl_info = {
    "name": "LED Strip Controller",
    "author": "Katterton",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "Properties > Output",
    "description": "A Blender plugin for controlling LED strips connected to an Arduino board, with automatic code generation."",
    "warning": "",
    "wiki_url": "",
    "category": "Lighting",
}

def register():
    bpy.utils.register_class(LedStrip)
    bpy.utils.register_class(ArduinoDevice)
    bpy.utils.register_class(AddArduinoDeviceOperator)
    bpy.utils.register_class(RemoveArduinoDeviceOperator)
    bpy.utils.register_class(AddLedStripMaterialOperator)
    bpy.utils.register_class(RemoveLedStripOperator)
    bpy.utils.register_class(ArduinoDevicePanel)
    bpy.utils.register_class(AddLedStripOperator)
    bpy.utils.register_class(StartStopOperator)
    bpy.utils.register_class(GenerateArduinoCodeOperator)

    bpy.types.Scene.arduino_devices = bpy.props.CollectionProperty(type=ArduinoDevice)
    

def unregister():
    del bpy.types.Scene.arduino_devices
    bpy.utils.unregister_class(ArduinoDevicePanel)
    bpy.utils.unregister_class(RemoveLedStripOperator)
    bpy.utils.unregister_class(AddLedStripMaterialOperator)
    bpy.utils.unregister_class(RemoveArduinoDeviceOperator)
    bpy.utils.unregister_class(AddArduinoDeviceOperator)
    bpy.utils.unregister_class(ArduinoDevice)
    bpy.utils.unregister_class(LedStrip)
    bpy.utils.unregister_class(AddLedStripOperator)
    bpy.utils.unregister_class(StartStopOperator)
    bpy.utils.unregister_class(GenerateArduinoCodeOperator)


if __name__ == "__main__":
    register()