ILoveTwitterLamp
================

A "Just For Fun" project using a RaspberryPi, a relay board, a lamp (or similar mains appliance) and the Python Twitter API found here: https://pypi.python.org/pypi/twitter/

When the user whose Twitter account is being used for API access receives a Direct Message with the words "I love lamp" the relay switch is activated, causing your lamp (or any other appliance attached to the relay board) to turn on. A check on the GPIO pins looks for a button press to reset the system (i.e. turn the lamp off) and await a new Direct Message to arrive.

Of course this isn't really about our shared love for lamps, it's a simple example of a real world reaction to the virtual world.
