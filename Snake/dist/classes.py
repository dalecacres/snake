import random

BUTTON_SIZE = 100
BLOCK_SIZE = 30
BLOCK_NUM = 30
MAP_SIZE = BLOCK_NUM * BLOCK_SIZE

def empty_space(array_like):
	size = BLOCK_SIZE * MAP_SIZE
	all_spaces = [Vector(row * BLOCK_SIZE, col * BLOCK_SIZE) for col in range(BLOCK_NUM) for row in range(BLOCK_NUM)]
	for i, cell in enumerate(array_like):
		x = int(cell.x / BLOCK_SIZE)
		y = int(cell.y / BLOCK_SIZE)
		all_spaces[y * BLOCK_NUM + x] = "snake"

	all_spaces = list(filter(lambda el: el != "snake", iter(all_spaces)))
	return all_spaces


class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def plus(self, vector):
		self.x = self.x + vector.x
		self.y = self.y + vector.y
		return self

class Score:
	def __init__(self, high_score):
		self.value = 0
		self.high_score = high_score
	def update(self):
		self.value += 2
		if self.value > self.high_score:
			self.high_score = self.value
	def get(self):
		return self.value
	def get_hs(self):
		return self.high_score

class Food:
	def __init__(self, snake_array):
		space = empty_space(snake_array)
		element = random.randint(0, len(space))
		self.position = space[element]
	def update(self, snake_array):
		space = empty_space(snake_array)
		element = random.randint(0, len(space))
		self.position = space[element]

class Snake:
	def __init__(self):
		self.direction = 'left'
		self.modifier = Vector(-BLOCK_SIZE, 0)
		self.cells = [Vector(MAP_SIZE / 2, MAP_SIZE / 2)]

	def set_dir(self, vector, dir):
		self.modifier = vector
		self.direction = dir
	
	def get_dir(self):
		return self.direction
	
	def update(self):
		self.cells.append(Vector(self.cells[-1].x + self.modifier.x, self.cells[-1].y + self.modifier.y))
		del self.cells[0]

		if self.cells[-1].x > MAP_SIZE - BLOCK_SIZE:
			self.cells[-1].x = 0
		if self.cells[-1].y > MAP_SIZE - BLOCK_SIZE:
			self.cells[-1].y = 0
		if self.cells[-1].x < 0:
			self.cells[-1].x = MAP_SIZE
		if self.cells[-1].y < 0:
			self.cells[-1].y = MAP_SIZE

	def grow(self):
		self.cells.insert(0, Vector(self.cells[-1].x + self.modifier.x * -1, self.cells[-1].y + self.modifier.y * -1))
		self.cells.insert(0, Vector(self.cells[-1].x + self.modifier.x * -1, self.cells[-1].y + self.modifier.y * -1))

	def overlap(self, vector):
		return self.cells[-1].x >= vector.x and self.cells[-1].x <= (vector.x + 1) and self.cells[-1].y >= vector.y and self.cells[-1].y <= (vector.y + 1)

