from Vehicle import Vehicle
from Escort import Escort
from model.ConvoyRobberyModel import ConvoyRobberyModel

class SmallConvoy(Vehicle):
	def __init__(
		self,
		unique_id: int,
		model: ConvoyRobberyModel,
		attack: float = 10,
		defense: float = 5,
		base_speed: float = 2
	) -> None:
		super().__init__(unique_id, model, attack, defense, base_speed)
		self.num_escorts = 1
		self.escorts: list[Escort] = []

	def assign_escorts(self, escorts) -> None:
		if len(self.escorts) < self.num_escorts:
			self.escorts = escorts
			for escort in self.escorts:
				escort: Escort
				escort.convoy = self

	def move(self):
		new_position = (0, 0)
		self.model.grid.move_agent(self, new_position)