import bpy
from .operators import StartStopOperator
class ArduinoDevicePanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_arduino_devices"
    bl_label = "Arduino LED Strip Controller"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    @classmethod
    def poll(cls, context):
        return context.space_data.context == 'OUTPUT'

    def draw(self, context):
        layout = self.layout

        layout.operator("arduino_device.add_device", text="Add Device")

        for device in bpy.context.scene.arduino_devices:
            device_box = layout.box()

            row = device_box.row()
            row.label(text="IP Address:")
            row.prop(device, "ip_address", text="")

            row = device_box.row()
            row.label(text="Port:")
            row.prop(device, "port", text="")

            row = device_box.row()
            add_led_strip_op = row.operator("arduino_device.add_led_strip", text="Add LED Strip")
            if add_led_strip_op:
                add_led_strip_op.device_index = device.index

            led_strips_column = device_box.column(align=True)
            for led_strip in device.led_strips:
                led_strip_box = device_box.box()
                row = led_strip_box.row()
                row.prop(led_strip, "index", text="Index")

                row.prop(led_strip, "num_leds")

                add_material_op = row.operator("arduino_device.add_led_strip_material", text="Add Material")

                if add_material_op:
                    add_material_op.device_index = device.index
                    add_material_op.led_strip_index = led_strip.index
                row.prop(led_strip, "material")
                remove_led_strip_op = row.operator("arduino_device.remove_led_strip", text="", icon="X")
                if remove_led_strip_op:
                    remove_led_strip_op.device_index = device.index
                    remove_led_strip_op.led_strip_index = led_strip.index

            row = device_box.row()
            remove_device_op = row.operator("arduino_device.remove_device", text="Remove Device", icon="X")
            if remove_device_op:
                remove_device_op.device_index = device.index

            row = device_box.row()
            start_stop_op = row.operator(StartStopOperator.bl_idname, text="Start/Stop")
            start_stop_op.device_index = device.index

            row = device_box.row()
            generate_code_op = row.operator("arduino_device.generate_arduino_code", text="Copy Arduino Code")
            generate_code_op.device_index = device.index
