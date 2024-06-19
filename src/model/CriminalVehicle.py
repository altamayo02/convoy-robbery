from Vehicle import Vehicle
from model.ConvoyRobberyModel import ConvoyRobberyModel

class CriminalVehicle(Vehicle):
	def __init__(
		self,
		unique_id: int,
		model: ConvoyRobberyModel,
		attack: float,
		defense: float,
		base_speed: float
	) -> None:
		super().__init__(unique_id, model)
		self.model: ConvoyRobberyModel
		self.attack = attack
		self.defense = defense
		self.speed = base_speed
	
	def move(self):
		pass
	
	def attack_vehicle(self):
		cellmates = self.model.grid.get_cell_list_contents([self.pos])
		cellmates.pop(
			cellmates.index(self)
		)
		if len(cellmates) > 0:
			# FIXME - Attacks go here
			pass
	
	def step(self):
		self.move()
		# Attack, defend, etc.