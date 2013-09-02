class Plugin:
	active = False

	def __init__(self, controller):
		self.controller = controller

	def on_message(self, msg):
		if msg.startswith("--example"):
			self.controller.send_message("Hi, from Example!")