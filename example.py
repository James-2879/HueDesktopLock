from HueDesktopLock import *

hue = PhilipsHue(bridge_address = "192.168.0.6", # change to your bridge IP
                lights = [15, 16, 17]) # see module documentation https://github.com/studioimaginaire/phue
control = CustomControl(hue = hue, # do not edit unless you change the PhilipsHue instance name
                        name = "Hue Python Desktop Lock")
control.runner()
