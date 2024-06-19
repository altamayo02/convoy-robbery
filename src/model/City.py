import math, json, random
from collections import deque

#Dijkstra, Floyd-Warshall, Bellman-Ford
#Prim, Kruskal, Vorubka

class City:
	def __init__(self, width: int = 0, height: int = 0):
		self.intersections: dict[any, dict[any, any]] = {}
		self.width = width
		self.height = height

		for y in range(self.height):
			for x in range(self.width):
				self.intersections[x, y] = {}
				for dy in [-1, 0, 1]:
					for dx in [-1, 0, 1]:
						if self.is_valid(y + dy, x + dx):
							self.intersections[x, y][x + dx, y + dy] = random.randint(0, 99) #math.inf
							if (x + dx, x + dy) not in self.intersections:
								self.intersections[x + dx, x + dy] = {}
							self.intersections[x + dx, x + dy][x, y] = random.randint(0, 99) #math.inf
	
	def get_nodes(self):
		return self.intersections
	
	def get_shallow_nodes(self):
		return list(self.intersections.keys())

	def get_adjacents(self, node):
		return self.intersections[node].items()

	def get_shallow_adjacents(self, node):
		return list(self.intersections[node].keys())

	def add(self, node):
		if node not in self.intersections:
			self.intersections[node] = {}
	
	def connect(self, v1, v2, weight = None):
		if v1 in self.intersections and v2 in self.intersections:
			self.intersections[v1][v2], self.intersections[v2][v1] = weight, weight
	
	def disconect(self, v1, v2):
		del self.intersections[v1][v2], self.intersections[v2][v1]
	
	def is_valid(self, x, y):
		return (
			0 <= x < self.width and
			0 <= y < self.height
		)

	def breadth_first_search(self, origin):
		queue = deque([origin])
		# Conjunto: Colección de elementos únicos
		traversed = set()
		traversal = []
		while queue:
			node = queue.popleft()
			traversal.append(node)
			traversed.add(node)
			for adj in self.get_shallow_adjacents(node):
				if adj not in queue and adj not in traversed:
					# Encolar
					queue.append(adj)
		
		return traversal
	
	def depth_first_search(self, origin):
		stack = [origin]
		traversed = set()
		traversal = []
		while stack:
			node = stack.pop()
			traversal.append(node)
			traversed.add(node)
			for adj in self.get_shallow_adjacents(node):
				if adj not in stack and adj not in traversed:
					# Apilar
					stack.append(adj)
		
		return traversal

	def dijkstra(self, origin):
		queue = [(0, origin)]
		traversed = set()
		distances = {node: float('inf') for node in self.intersections}
		distances[origin] = 0
		while queue:
			curr_dist, node = min(queue)
			queue.remove((curr_dist, node))
			if node not in traversed:
				traversed.add(node)
				for adj, dist_to_adj in self.get_adjacents(node):
					new_dist = curr_dist + dist_to_adj
					if new_dist < distances[adj]:
						distances[adj] = new_dist
						queue.append((new_dist, adj))
		return distances

	def floyd_warshall(self):
		distances = {
			n1: {n2: float('inf') for n2 in self.intersections} for n1 in self.intersections
		}
		for node in self.intersections:
			distances[node][node] = 0
			for adj in self.get_shallow_adjacents(node):
				distances[node][adj] = self.intersections[node][adj]
		for k in self.intersections:
			for i in self.intersections:
				for j in self.intersections:
					distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])
		return distances

	def bellman_ford(self, origin):
		distances = {node: float('inf') for node in self.intersections}
		distances[origin] = 0

		for _ in range(len(distances) - 1):
			for node in self.intersections:
				for adj, dist_to_adj in self.get_adjacents(node):
					new_dist = distances[node] + dist_to_adj
					if new_dist < distances[adj]:
						distances[adj] = new_dist
		return distances
	
	def prim(self, origin):
		candidates = []
		for adj, dist_to_adj in self.get_adjacents(origin):
			candidates.append((dist_to_adj, origin, adj))
		
		traversed = set()
		traversed.add(origin)
		min_span_tree = []
		while candidates:
			candidates.sort()
			distance, start, end = candidates.pop(0)

			if end not in traversed:
				traversed.add(end)
				min_span_tree.append((start, end, distance))

				for adj, dist_to_adj in self.get_adjacents(end):
					if adj not in traversed:
						candidates.append((dist_to_adj, end, adj))
		return min_span_tree
	
	def kruskal(self):
		edges = []
		for start in self.intersections:
			for end, distance in self.get_adjacents(start):
				edges.append((distance, start, end))
		edges.sort()

		sets = [{node} for node in self.intersections]
		min_span_tree = []
		for distance, start, end in edges:
			start_set = None
			end_set = None

			for set in sets:
				if start in set:
					start_set = set
				if end in set:
					end_set = set

			if start_set != end_set:
				min_span_tree.append((start, end, distance))
				start_set.update(end_set)
				sets.remove(end_set)
		return min_span_tree
	
	# https://www.geeksforgeeks.org/boruvkas-mst-in-python/
	""" def boruvka(self):
		ranks = []
		parent_tree = []
		for node in self.nodes:
			parent_tree.append(node)
			ranks.append(0)

		shortest = [-1 for _ in self.nodes]
		num_trees = len(self.nodes)
		while num_trees > 1:
			for i in range(len()) """
	
	def __str__(self) -> str:
		string = ""
		for y in range(self.height):
			interlining = ""
			for x in range(self.width):
				connection = "    "
				if (x + 1, y) in self.get_shallow_adjacents((x, y)):
					connection = f"-{self.intersections[x, y][x + 1, y]:2.0f}-"
				string += f"{(x, y)}{connection}"

				if (x, y + 1) in self.get_shallow_adjacents((x, y)):
					interlining += f" {self.intersections[x, y][x, y + 1]:2.0f}|      "
				else:
					interlining += "          "
			string += f"\n{interlining}\n"
		return string

	def set_default(self):
		self = City(10, 10)
		self.disconect((0, 2), (0, 3))
		self.disconect((0, 3), (0, 4))
		self.disconect((0, 6), (0, 7))
		self.disconect((0, 7), (0, 8))

		self.disconect((1, 2), (1, 3))
		self.disconect((1, 6), (1, 7))

		self.disconect((2, 0), (2, 1))
		self.disconect((2, 8), (2, 9))

		self.disconect((3, 2), (3, 3))
		self.disconect((3, 5), (3, 6))

		self.disconect((4, 1), (4, 2))
		self.disconect((4, 2), (4, 3))
		self.disconect((4, 3), (4, 4))
		self.disconect((4, 5), (4, 6))
		self.disconect((4, 6), (4, 7))
		self.disconect((4, 7), (4, 8))
		self.disconect((4, 8), (4, 9))


		self.disconect((6, 1), (6, 2))
		self.disconect((6, 4), (6, 5))
		self.disconect((6, 8), (6, 9))

		self.disconect((7, 0), (7, 1))
		self.disconect((7, 2), (7, 3))
		self.disconect((7, 4), (7, 5))
		self.disconect((7, 6), (7, 7))
		self.disconect((7, 8), (7, 9))

		self.disconect((8, 1), (8, 2))
		self.disconect((8, 2), (8, 3))
		self.disconect((8, 4), (8, 5))
		self.disconect((8, 5), (8, 6))
		self.disconect((8, 7), (8, 8))
		self.disconect((8, 8), (8, 9))

		self.disconect((5, 4), (6, 4))
		self.disconect((5, 6), (6, 6))
		self.disconect((5, 9), (6, 9))

		self.disconect((7, 0), (8, 0))
		self.disconect((7, 1), (8, 1))
		self.disconect((7, 4), (8, 4))
		self.disconect((7, 6), (8, 6))
		self.disconect((7, 8), (8, 8))