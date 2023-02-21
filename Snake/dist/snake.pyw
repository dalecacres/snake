import time
import re
from classes import *
from draw import *

BUTTON_SIZE = 100
BLOCK_SIZE = 30
MAP_SIZE = 900

from pygame.locals import (
	K_UP,
	K_DOWN,
	K_LEFT,
	K_RIGHT,
	KEYDOWN,
	QUIT
)


def map_key(key, snake):
	map = {K_UP: Vector(0, -BLOCK_SIZE), 
		K_DOWN: Vector(0, BLOCK_SIZE),
		K_LEFT: Vector(-BLOCK_SIZE, 0), 
		K_RIGHT: Vector(BLOCK_SIZE, 0)
	}
	direction = {K_UP: 'up', 
		K_DOWN: 'down',
		K_LEFT: 'left', 
		K_RIGHT: 'right'
	}
	no_move = {
		'up': 'down',
		'down': 'up',
		'left': 'right',
		'right': 'left'
	}

	if key in map:
		if no_move[snake.get_dir()] != direction[key]:
			snake.set_dir(map[key], direction[key])


def update(draw, snake, food, user):
	snake.update()
	if snake.overlap(food.position):
		food.update(snake.cells)
		snake.grow()
		user['score'] += 2
	for cell in snake.cells[0:-2]:
		if snake.overlap(cell):
			return False
	draw.game(food, snake, user)
	pygame.display.flip()
	return True

def start_menu(draw):
	dictionary = {}
	users = {}
	user_list = []
	with open(r'C:/Users/Patient/Snake/dist/highscores.txt', 'r') as record:
		for line in record:
			name, score = line.split(',')
			score = int(re.sub('[^0-9]','', score))
			dictionary[score] = name
		record.close()
	user_keys = reversed(sorted(dictionary))
	for key in user_keys:
		users[key] = dictionary[key]
	scores = list(users.keys())	

	for i, score in enumerate(users):
		user_info = {
			'name': users[score],
			'rival': users[scores[i - 1]],
			'rival_score': scores[i - 1],
			'champion': users[scores[0]],
			'champion_score': scores[0],
			'high_score': score,
			'score': 0
		}
		user_list.append(user_info)
		
	running = True
	while running:
		draw.background()
		coordinates = draw.menu(user_list)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				x, y = event.pos
				for pressed in coordinates:
					if x >= pressed['coordinates'].x and x <= pressed['coordinates'].x + BUTTON_SIZE and y >= pressed['coordinates'].y and y <= pressed['coordinates'].y + BUTTON_SIZE:
						game_loop(draw, pressed)
		pygame.display.flip()

def game_loop(draw, user):
	score = user
	snake = Snake()
	food = Food(snake.cells)
	now = time.time()
	running = True
	while running:
		sec = time.time() - now
		if sec * BLOCK_SIZE / 3 > 1:
			now = time.time()
			running = update(draw, snake, food, score)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				map_key(event.key, snake)
			elif event.type == pygame.QUIT:
				running = False
	with open('C:/Users/Patient/Snake/dist/highscores.txt', 'r+') as record:
		for line in record:
			test = line.split(',')
			if user['name'] == test[0]:
				score = user['score']
				high_score = int(re.sub('[^0-9]','', test[1]))
				if score > int(high_score):
					record.write(user['name'] + ',' + str(score) + ';')
		record.truncate()
		record.close()

def main():
	draw = Draw()
	active = True
	while active:
		active = start_menu(draw)

if __name__ == '__main__':
	__main__ = main()