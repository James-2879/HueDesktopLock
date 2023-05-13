# HuePyDesktopLock

Initial draft.

## Overview

Collection of methods to control Philips Hue lights based on whether a computer has been locked via 'Win + L' shortcut.

Monitors for Win + L shortcut press (lock computer) to turn off lights, and then monitors for _any_ key inputs to turn lights back on.

### Caveats

Nothing will execute if machine is not locked via Win + L.

Windows and thereby Python do not have any functions that can return whether a computer is unlocked or not (https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-lockworkstation?redirectedfrom=MSDN). Some hacks are floating around StackOverflow for this, but these are very hit-and-miss. It is possible to monitor `LogonUI.exe` or the top window using Python library `ctypes`, but these workarounds are very resource intensive for what they do. Monitoring a keyboard shortcut is much less expensive.

## Usage

1. Clone repo `git clone <link>`.
2. Install dependencies `pip install -r requirements.txt`.
3. Configure arguments as required.

This project can be imported as a module (see `example.py`), or you can copy the classes directly from `HuePyDesktopLock.py` and edit as required.

Ensure you press the pairing button on your Hue Bridge before running for the first time.

### Philips Hue light control

Uses this module https://github.com/studioimaginaire/phue .

You will need to know your bridge IP address, and light indexes (see above documentation). If I have some time in the future I write some extra methods to automatically discover bridge/lights etc.
