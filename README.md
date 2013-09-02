ShazBot
=======

An extendable IRC bot with plugin capabilities. An example plugin is as follows:
```python
class Plugin:
	# The active variable signifies whether or not the plugin will be active
	# upon loading it.
    active = True

    def __init__(self, controller):
    	# The controller is passed in from the main class and is responsible for all
    	# IRC related operation, in particular channel messaging.
    	self.controller = controller

    def on_message(self, msg):
    	# on_message takes in a msg parameter. This method is called when a message is
    	# sent to the channel. The msg parameter simply refers to that message.
    	self.controller.send_message("Hello, World!")
```