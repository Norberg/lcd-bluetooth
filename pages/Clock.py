import time

import Base

class Clock(Base.Page):
	def __init__(self, display):
		Base.Page.__init__(self, display)
		self.freq = 0.5

	def update(self):
		self.setline(0,"Klockan ar:")
		t = time.strftime("%H:%M:%S")
		self.setline(1,t)
