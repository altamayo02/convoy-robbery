from mesa import Agent
from ConvoyRobberyModel import ConvoyRobberyModel

from Station import Station
from City import City

class Vehicle(Agent):
	def __init__(
		self,
		unique_id: int,
		model: ConvoyRobberyModel,
		attack: float,
		defense: float,
		weight: float,
		city: City,
	) -> None:
		super().__init__(unique_id, model)
		self.model: ConvoyRobberyModel
		self.attack = attack
		self.defense = defense
		self.weight = weight
		self.city = city
	
	def move(self):
		"""
			Defines the way the agent traverses the graph.
		"""
		pass
	
	def step(self):
		"""
			Executed every iteration. Dictates the actions of the agent.
		"""
		self.city.dijkstra()
	