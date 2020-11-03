class Process(object):
	def __init__(self, name, delay):
		self.name = name
		self.req = {}
		self.results = {}
		self.score = {} # ??
		self.delay = delay

	def	need(self, name, quantity):
		self.needs[name] = quantity
		if name in self.score:
			self.score[name] -= (quantity / self.delay)
		else:
			self.score[name] = -(quantity / self.delay)
		return self

	def	result(self, name, quantity):
		self.results[name] = quantity
		if name in self.score:
			self.score[name] += (quantity / self.delay)
		else:
			self.score[name] = (quantity / self.delay)
		return self
