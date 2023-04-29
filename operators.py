import bpy
class StartStopOperator(bpy.types.Operator):
    bl_idname = "arduino_device.start_stop"
    bl_label = "Start/Stop"

    device_index: bpy.props.IntProperty()

    def execute(self, context):
        target_device = None
        for device in bpy.context.scene.arduino_devices:
            if device.index == self.device_index:
                target_device = device
                break

        if target_device:
            if target_device.is_running:
                target_device.stop()
            else:
                target_device.start()

            # Update the UI
            bpy.context.area.tag_redraw()
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, f"Arduino device with index {self.device_index} not found.")
            return {'CANCELLED'}

    def draw(self, context):
        layout = self.layout
        target_device = None
        for device in context.scene.arduino_devices:
            if device.index == self.device_index:
                target_device = device
                break

        if target_device:
            if target_device.is_running:
                layout.label(text="Sending data...")
                layout.operator(self.bl_idname, text="Stop").device_index = self.device_index
            else:
                layout.operator(self.bl_idname, text="Start").device_index = self.device_index
        else:
            layout.label(text=f"Arduino device with index {self.device_index} not found.")

            
            
            
            
            
            
class AddArduinoDeviceOperator(bpy.types.Operator):
    bl_idname = "arduino_device.add_device"
    bl_label = "Add Device"
    
    ip_address: bpy.props.StringProperty(name="IP Address", default="192.168.0.105")
    port: bpy.props.IntProperty(name="Port", default=4210)
    
    def execute(self, context):
        num_devices = len(context.scene.arduino_devices)
        device = context.scene.arduino_devices.add()
        device.ip_address = self.ip_address
        device.port = self.port
        device.index = num_devices
        device.sock = None
        return {'FINISHED'}


class RemoveArduinoDeviceOperator(bpy.types.Operator):
    bl_idname = "arduino_device.remove_device"
    bl_label = "Remove Device"
    device_index: bpy.props.IntProperty()

    def execute(self, context):
        print(f"Removing Arduino device with index {self.device_index}...")  # Add this line
        for i, device in enumerate(context.scene.arduino_devices):
            if device.index == self.device_index:
                context.scene.arduino_devices.remove(i)
                break
        return {'FINISHED'}

class AddLedStripMaterialOperator(bpy.types.Operator):
    bl_idname = "arduino_device.add_led_strip_material"
    bl_label = "Add LED Strip Material"
    led_strip_index: bpy.props.IntProperty()
    device_index: bpy.props.IntProperty()

    def execute(self, context):
        device = context.scene.arduino_devices[self.device_index]
        led_strip = device.led_strips[self.led_strip_index]
        material_name = f"LED_Strip_Material_{device.index}_{led_strip.index}"
        
        material = bpy.data.materials.get(material_name)
        if not material:
            material = bpy.data.materials.new(name=material_name)
            material.use_nodes = True
            
            # Delete the Principled BSDF node
            tree = material.node_tree
            nodes = tree.nodes
            principled_node = nodes.get("Principled BSDF")
            if principled_node is not None:
                nodes.remove(principled_node)
            
            # Add a ColorRamp node to the material
            color_ramp_node = nodes.new(type="ShaderNodeValToRGB")
            material_output_node = nodes.get("Material Output")
            links = tree.links
            links.new(color_ramp_node.outputs[0], material_output_node.inputs[0])
        
        # Add the material to the newly created LED strip
        led_strip.material = material
        
        return {'FINISHED'}







class RemoveLedStripOperator(bpy.types.Operator):
    bl_idname = "arduino_device.remove_led_strip"
    bl_label = "Remove LED Strip"
    led_strip_index: bpy.props.IntProperty()
    device_index: bpy.props.IntProperty()

    def execute(self, context):
        device = context.scene.arduino_devices[self.device_index]
        device.led_strips.remove(self.led_strip_index)
        return {'FINISHED'}
    
class GenerateArduinoCodeOperator(bpy.types.Operator):
    bl_idname = "arduino_device.generate_arduino_code"
    bl_label = "Copy Arduino Code"

    device_index: bpy.props.IntProperty()

    def execute(self, context):
        device = context.scene.arduino_devices[self.device_index]
        if device:
            arduino_code = device.generate_arduino_code()
            bpy.context.window_manager.clipboard = arduino_code
        return {'FINISHED'}       

                
               
class AddLedStripOperator(bpy.types.Operator):
    bl_idname = "arduino_device.add_led_strip"
    bl_label = "Add LED Strip"
    device_index: bpy.props.IntProperty()

    def execute(self, context):
        device = context.scene.arduino_devices[self.device_index]
        led_strip = device.led_strips.add()
        led_strip.index = len(device.led_strips) - 1
        return {'FINISHED'}