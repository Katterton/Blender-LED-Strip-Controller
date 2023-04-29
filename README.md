# Arduino LED Strip Control Add-on for Blender

This is a Blender add-on that allows you to control LED strips connected to an Arduino board. The add-on generates Arduino code that can be uploaded to the board, allowing you to control the LED strips from within Blender.

## Features

- Assign materials to LED strips in Blender
- Generate Arduino code to control LED strips
- Control LED strips from within Blender
- Supports multiple devices and LED strips

## Installation

1. Download the latest release from the [releases page](https://github.com/yourusername/your-repo/releases).
2. In Blender, go to `Edit` > `Preferences` > `Add-ons`.
3. Click `Install...` and select the downloaded ZIP file.
4. Enable the add-on by checking the checkbox next to it.

## Usage

1. Connect your Arduino board and LED strips to your computer.
2. In Blender, go to the Output tab.
3. Create a new Arduino device by clicking the Add Arduino button in the Arduino LED Strip Control panel.
4. Enter the IP address and port number of your Arduino device.
5. Create a new LED strip by clicking the Add LED Strip button in the Arduino LED Strip Control panel.
6. Change the pin numbers for the LED strip if necessary.
7. Assign a material to the LED strip.
8. Open the generated Arduino code in the Arduino IDE.
9. Enter your Wi-Fi network's SSID and password in the corresponding fields.
10. Upload the edited code to the Arduino board.
11. Edit the Color Ramp of the assigned material to change the LED strip's color.
12. The LED strips update on frame changes only, so hit the play button to send data to the Arduino board and control the LED strips from within Blender.

## License

This add-on is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
