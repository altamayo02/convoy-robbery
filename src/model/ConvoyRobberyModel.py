from mesa import Model, DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from City import City
from Station import Station


class ConvoyRobberyModel(Model):
	def __init__(self, width=10, height=10, criminal_attack=1, criminal_defense=1):
		super().__init__()
		self.grid: MultiGrid = MultiGrid(width, height, True)
		self.schedule: RandomActivation = RandomActivation(self)
		self.datacollector = DataCollector(
			model_reporters={
				#"Gini": compute_gini
			}, agent_reporters={
				"Wealth": "wealth"
			}
		)
		self.city = City(width, height)
		self.city.set_default()
		self.stations = []
		for _ in range(width):
			station = Station()
			self.add_station(station)
		self.running = True
		self.datacollector.collect(self)

	def add_vehicle(self, agent):
		self.schedule.add(agent)
		station = self.random.choice(self.stations)
		x, y = self.schedule.agents[station].pos
		self.grid.place_agent(agent, (x, y))
		station.vehicles.append(agent)

	def add_station(self, station):
		self.schedule.add(station)
		# Add the station to a random grid cell
		x = self.random.randrange(self.grid.width)
		y = self.random.randrange(self.grid.height)
		self.grid.place_agent(station, (x, y))
		self.stations.append(station)

	def step(self):
		self.schedule.step()
		# collect data
		self.datacollector.collect(self)