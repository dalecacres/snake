import pygame
from classes import Vector
BUTTON_SIZE = 100
BLOCK_SIZE = 30
MAP_SIZE = 900

class Draw:
	def __init__(self):
		icon = pygame.image.load(r'C:\Users\Patient\Snake\dist\snake.png')
		pygame.display.set_caption('Snake')
		pygame.display.set_icon(icon)
		pygame.init()

	def food(self, vector):
		pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(vector.x + BLOCK_SIZE / 4, vector.y + BLOCK_SIZE / 4, BLOCK_SIZE / 2, BLOCK_SIZE / 2))
	
	def snake(self, snake):
		for i, cell in enumerate(snake.cells):
			if len(snake.cells) > 3:
				if i == 0:
					pygame.draw.rect(self.screen, (0, 200, 50), pygame.Rect(cell.x + 5 / 1.5, cell.y + 5 / 1.5, (BLOCK_SIZE - 5) / 2.5, (BLOCK_SIZE - 5) / 2.5))
				elif i == 1:
					pygame.draw.rect(self.screen, (0, 200, 50), pygame.Rect(cell.x + 5 / 2, cell.y + 5 / 2, (BLOCK_SIZE - 5) / 2, (BLOCK_SIZE - 5) / 2))
				elif i == 2:
					pygame.draw.rect(self.screen, (0, 200, 50), pygame.Rect(cell.x + 5 / 2.5, cell.y + 5 / 2.5, (BLOCK_SIZE - 5) / 1.5, (BLOCK_SIZE - 5) / 1.5))
				else: 
					pygame.draw.rect(self.screen, (0, 200, 50), pygame.Rect(cell.x, cell.y, (BLOCK_SIZE - 5), (BLOCK_SIZE - 5)))
			else: 
				pygame.draw.rect(self.screen, (0, 200, 50), pygame.Rect(cell.x, cell.y, (BLOCK_SIZE - 5), (BLOCK_SIZE - 5)))

	def background(self):
		self.screen.fill((100, 150, 100))

	def game(self, food, snake, score):
		self.background()
		self.food(food.position)
		self.snake(snake)
		self.score(score)

	def score(self, score):
		font = pygame.font.Font('freesansbold.ttf', 30)
		self.text(font, score['name'], Vector(10, 20))
		self.text(font, str(score['score']), Vector(110, 20))
		self.text(font, str(score['high_score']), Vector(160, 20))
		font = pygame.font.Font('freesansbold.ttf', 20)
		if score['champion'] != score['name']:
			self.text(font, 'Rival:', Vector(10, 50))
			self.text(font, score['rival'], Vector(100, 50))
			self.text(font, str(score['rival_score']), Vector(150, 50))
			self.text(font, 'Champ:', Vector(10, 80))
			self.text(font, score['champion'], Vector(100, 80))
			self.text(font, str(score['champion_score']), Vector(150, 80))
	
	def text(self, font, text, vector):
		label = font.render(text, True,'white', (100, 150, 100))
		rect = label.get_rect()
		pygame.draw.rect(label, (0, 0, 0), rect, 1)
		self.screen.blit(label, (vector.x, vector.y))

	def button(self, user, vector):
		font = pygame.font.Font('freesansbold.ttf', 20)
		if user['name'] == 'plus':
			plus = font.render('+', True, 'white', (100, 150, 100))
			pygame.draw.rect(plus, (100, 150, 100), pygame.Rect(0, 0, BUTTON_SIZE, BUTTON_SIZE), 1)
			self.screen.blit(plus, (vector.x, vector.y))
		else:
			name_rect = pygame.Rect(vector.x, vector.y, vector.x + BUTTON_SIZE, vector.y + BUTTON_SIZE)
			name = font.render(user['name'], True, 'white', (100, 150, 100))
			score = font.render(str(user['high_score']), True, 'white', (100, 150, 100))
			pygame.draw.rect(name, (100, 150, 100), pygame.Rect(0, 0, BUTTON_SIZE, BUTTON_SIZE), 1)
			pygame.draw.rect(score, (100, 150, 100), pygame.Rect(0, 0, BUTTON_SIZE, BUTTON_SIZE), 1)
			self.screen.blit(name, (vector.x, vector.y))
			self.screen.blit(score, (vector.x, vector.y + 40))
		user['coordinates'] = vector
		return user

	def menu(self, users):
		coordinates = []
		for i, user in enumerate(users):
			coordinates.append(self.button(user, Vector(i % 5 * BUTTON_SIZE + MAP_SIZE / 7, i // 5  * BUTTON_SIZE + MAP_SIZE / 4)))
		coordinates.append(self.button({'name': 'plus'}, Vector((i + 1) % 5 * BUTTON_SIZE + MAP_SIZE / 7, (i + 1) // 5 * BUTTON_SIZE + MAP_SIZE / 4)))

		return coordinates

class InputBox:
	def __init__(self, x, y, w, h, text=''):
		COLOR_INACTIVE = pygame.Color('lightskyblue3')
		COLOR_ACTIVE = pygame.Color('dodgerblue2')
		FONT = pygame.font.Font('freesansbold.ttf', 32)
		screen = pygame.display.set_mode([MAP_SIZE, MAP_SIZE])
		self.rect = pygame.Rect(x, y, w, h)
		self.color = COLOR_INACTIVE
		self.text = text
		self.txt_surface = FONT.render(text, True, self.color)
		self.active = False

	def handle_event(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			# If the user clicked on the input_box rect.
			if self.rect.collidepoint(event.pos):
				# Toggle the active variable.
				self.active = not self.active
			else:
				self.active = False
			# Change the current color of the input box.
			self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
		if event.type == pg.KEYDOWN:
			if self.active:
				if event.key == pg.K_RETURN:
					self.text = ''
				elif event.key == pg.K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					self.text += event.unicode
				# Re-render the text.
				self.txt_surface = FONT.render(self.text, True, self.color)
