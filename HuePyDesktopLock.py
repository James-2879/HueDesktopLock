import ctypes
from phue import Bridge # https://github.com/studioimaginaire/phue
from pynput import keyboard

class PhilipsHue:
    def __init__(self, bridge_address: str, lights: list):
        self.bridge_address = bridge_address
        self.lights = lights
        try:
            self.bridge = Bridge(self.bridge_address)
            self.bridge.connect()
        except BaseException:
            print("Press pairing button on hub before running.")
            ctypes.windll.user32.MessageBoxW(0, "Press pairing button on hub before running.", 0)

    def turn_off(self):
        self.bridge.set_light(self.lights, "on", False)
        
    def turn_on(self):
        self.bridge.set_light(self.lights, "on", True)

    def dim_lights(self):
        current_brightness = self._get_light_brightness()
        new_brightness = current_brightness - 10
        self.bridge.set_light(self.lights, "bri", new_brightness) 
        
    def raise_lights(self):
        current_brightness = self._get_light_brightness()
        new_brightness = current_brightness + 10
        self.bridge.set_light(self.lights, "bri", new_brightness) 
        
    def _get_light_brightness(self):
        brightness = self.bridge.get_light(self.lights[0])["state"]["bri"]
        return(int(brightness))
        
class CustomControl:
    """
    Monitor for only a single combination.
    Key presses are not logged to reduce security vulnerability.    
    """
    def __init__(self, hue, command = ["Key.cmd", "Key.cmd_r"], modifier = "'l'", name: str = None):
        """
        Parameters:
            command: string or list (of strings)
            modifier: string or list (of strings)
            hue: instance of PhilipsHue class
            name: string of program name for error messages
        """
        self.command = command
        self.modifier = modifier
        self.name = name
        self.locked = False
        self.command_down = False
        self.hue = hue

    def runner(self):
        with keyboard.Listener(
        on_press=self._on_press,
        on_release=self._on_release) as listener:
            listener.join()

    def _on_press(self, key):
        if self.locked:
            self._react_on()
        if self.command_down and str(key) == self.modifier:
            self.command_down = False   
            self._react_off()         
        if str(key) in self.command:
            self.command_down = True

    def _on_release(self, key):
        if str(key) in self.command:
            self.command_down = False
            
    def _react_on(self):
        try:
            self.hue.turn_on()
        except Exception as error:
            self._error(error)
            raise SystemExit
        finally:
            self.locked = False
            
    def _react_off(self):
        try:
            self.hue.turn_off()
        except Exception as error:
            self._error(error)
            raise SystemExit
        finally:
            self.locked = True
          
    def _error(self, error):
        print(error)
        ctypes.windll.user32.MessageBoxW(0, "Program was unable to complete execution, please see error below:\n\n"+str(error)+"\n\nProgram will terminate.", self.name, 0)
        
if __name__ == "__main__":    
    hue = PhilipsHue(bridge_address = "192.168.0.6",
                     lights = [15, 16, 17])
    control = CustomControl(hue = hue,
                            name = "Python Light Control")
    control.runner()