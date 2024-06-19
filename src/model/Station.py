import random

from BigConvoy import BigConvoy
from SmallConvoy import SmallConvoy
from Escort import Escort
from City import City

class Station:
	def __init__(self, city: City) -> None:
		self.goods = random.randint(0, 10000)
		self.city = city
		self.convoys = []
		self.escorts = []

	def add_vehicle(self, vehicle):
		if type(vehicle) in [BigConvoy, SmallConvoy]:
			self.convoys.append(vehicle)
		elif type(vehicle) == Escort:
			self.escorts.append(vehicle)

	def ship(self):
		shipment = random.randint(0, self.goods)
		self.goods -= shipment
		return shipment