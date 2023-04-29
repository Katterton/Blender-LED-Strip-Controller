import bpy

class LedStrip(bpy.types.PropertyGroup):
    num_leds: bpy.props.IntProperty(name="Number of LEDs", default=10)
    index: bpy.props.IntProperty(name="index", default=0)
    material: bpy.props.PointerProperty(type=bpy.types.Material, name="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)