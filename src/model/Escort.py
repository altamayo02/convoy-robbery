from Vehicle import Vehicle
from model.ConvoyRobberyModel import ConvoyRobberyModel

class Escort(Vehicle):
	def __init__(
		self,
		unique_id: int,
		model: ConvoyRobberyModel,
		attack: float = 5,
		defense: float = 5,
		base_speed: float = 3
	) -> None:
		super().__init__(unique_id, model, attack, defense, base_speed)
		self.convoy: Vehicle = None

	def move(self):
		new_position = self.convoy.pos
		self.model.grid.move_agent(self, new_position)