
import socket
import bpy
from .led_strip import LedStrip
class ArduinoDevice(bpy.types.PropertyGroup):
    is_running: bpy.props.BoolProperty(default=False)
    ip_address: bpy.props.StringProperty(name="IP Address", default="192.168.0.105")
    port: bpy.props.IntProperty(name="Port", default=4210)
    index: bpy.props.IntProperty(name="index", default=0)
    led_strips: bpy.props.CollectionProperty(type=LedStrip)
    sock: socket.socket = None

    def start(self):
        if not self.is_running:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bpy.app.handlers.frame_change_pre.append(self.send_color_data)
            self.is_running = True

    def stop(self):
        if self.is_running:
            if self.send_color_data in bpy.app.handlers.frame_change_pre:
                bpy.app.handlers.frame_change_pre.remove(self.send_color_data)
            self.is_running = False

    def send_color_data(self,x,y):
        for led_strip in self.led_strips:
            material = led_strip.material
            color_ramp = material.node_tree.nodes["ColorRamp"]
            packet = bytearray(1 + led_strip.num_leds * 3)
            packet[0] = led_strip.index+1
            led_index = 0
            for i in range(led_strip.num_leds):
                x = i * (1/led_strip.num_leds)
                color = color_ramp.color_ramp.evaluate(x)[:3]
                r, g, b = [int(c * 255) for c in color]
                packet[1 + led_index * 3] = b
                packet[2 + led_index * 3] = r
                packet[3 + led_index * 3] = g
                led_index += 1
                if led_index >= led_strip.num_leds:
                    break
            self.sock.sendto(packet, (self.ip_address, self.port))
    def generate_arduino_code(self):
        arduino_code = ''
        arduino_code += '#include <ESP8266WiFi.h>\n'
        arduino_code += '#include <WiFiUdp.h>\n'
        arduino_code += '#include <FastLED.h>\n'
        arduino_code += '\n'
        for i, strip in enumerate(self.led_strips):
            arduino_code += '#define NUM_LEDS' + str(i+1) + ' ' + str(strip['num_leds']) + '\n'
            arduino_code += 'CRGB leds' + str(i+1) + '[NUM_LEDS' + str(i+1) + '];\n'
        arduino_code += '\n'
        arduino_code += 'const char* ssid = "' + self.ip_address + '";\n'
        arduino_code += 'const char* password = "' + str(self.port) + '";\n'
        arduino_code += 'const size_t pbuf_unit_size = 1024;\n'
        arduino_code += 'WiFiUDP Udp;\n'
        arduino_code += 'unsigned int localUdpPort = ' + str(self.port) + ';\n'
        arduino_code += 'char incomingPacket[1024];\n'
        arduino_code += 'char  replyPacket[] = "Hi there! Got the message :-)";\n'
        arduino_code += '\n'
        arduino_code += 'void initLEDs() {\n'
        for i, strip in enumerate(self.led_strips):
             arduino_code += '  FastLED.addLeds<NEOPIXEL, D' + str(i+2) + '>(leds' + str(i+1) + ', NUM_LEDS' + str(i+1) + ');\n'
        arduino_code += '}\n'
        arduino_code += '\n'
        arduino_code += 'void setup() {\n'
        arduino_code += '  Serial.begin(115200);\n'
        arduino_code += '  Serial.println();\n'
        arduino_code += '\n'
        arduino_code += '  // Connect to WiFi network\n'
        arduino_code += '  Serial.printf("Connecting to %s ", ssid);\n'
        arduino_code += '  WiFi.begin(ssid, password);\n'
        arduino_code += '  while (WiFi.status() != WL_CONNECTED)\n'
        arduino_code += '  {\n'
        arduino_code += '    delay(500);\n'
        arduino_code += '    Serial.print(".");\n'
        arduino_code += '  }\n'
        arduino_code += '  Serial.println(" connected");\n'
        arduino_code += '\n'
        arduino_code += '  // Initialize LEDs\n'
        arduino_code += '  initLEDs();\n'
        arduino_code += '\n'
        arduino_code += '  // Initialize UDP connection\n'
        arduino_code += '  Udp.begin(localUdpPort);\n'
        arduino_code += '  Serial.printf("Now listening at IP %s, UDP port %d\\n", WiFi.localIP().toString().c_str(), localUdpPort);\n'
        arduino_code += '}\n'
        arduino_code += '\n'
        arduino_code += 'void loop() {\n'
        arduino_code += '  int packetSize = Udp.parsePacket();\n'
        arduino_code += '  if (packetSize)\n  {\n'
        arduino_code += '    // receive incoming UDP packets\n'
        arduino_code += '    Serial.printf("Received %d bytes from %s, port %d\\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());\n'
        arduino_code += '    int len = Udp.read(incomingPacket, 255);\n'
        arduino_code += '    if (len > 0)\n'
        arduino_code += '    {\n'
        arduino_code += '      incomingPacket[len] = 0;\n'
        arduino_code += '    }\n'
        for i, strip in enumerate(self.led_strips):
            arduino_code += '    if (int(incomingPacket[0]) == ' + str(i+1) + ')\n'
            arduino_code += '    {\n'
            arduino_code += '      for (int j = 0; j < NUM_LEDS' + str(i+1) + '; j++)\n'
            arduino_code += '      {\n'
            arduino_code += '        leds' + str(i+1) + '[j] = CRGB(int(incomingPacket[3*j+2]), int(incomingPacket[3*j+3]), int(incomingPacket[3*j+1]));\n'
            arduino_code += '      }\n'
            arduino_code += '    }\n'
        arduino_code += '    FastLED.show();\n'
        arduino_code += '  }\n'
        arduino_code += '}\n'
        return arduino_code