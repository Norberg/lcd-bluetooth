from logger.recvReading import recvReading



import Base

class Temperature(Base.Page):
	def __init__(self, display):
		Base.Page.__init__(self, display)
		self.freq = 1

	def update(self):
		readings = recvReading(HOST="sheeva")
		indoor = float(readings['indoor'][1])
		outdoor = float(readings['outdoor'][1])
		self.setline(0,"Indoor:  %4.1f C" % indoor)
		self.setline(1,"Outdoor: %4.1f C" % outdoor)
