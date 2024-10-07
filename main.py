import pygame
import random
pygame.init()


screenWidth = 1000
screenHeight = 600
gameWindow = pygame.display.set_mode((screenWidth,screenHeight))

highScore = 0
with open("resources/tmp/highScore.txt", "r") as f:
	highScore = f.read()

if highScore !=0:
	pygame.display.set_caption(f"Snake Game | High Score : {highScore}")


pygame.display.set_caption("Snake Game")
pygame.display.update()


exitGame = False
gameOver = False

# color

white = (255,255,255)
red = (255, 0 , 0)
black = (0,0,0)

# game specific variables

x = 45
y = 45
size = 40
FPS=30
velocity_x = 0
velocity_y = 0
speed = 5
food_x = random.randint(0, screenWidth-200)
food_y = random.randint(0,screenHeight-200)

block = pygame.image.load("resources/image/block.jpg")
apple = pygame.image.load("resources/image/apple.png")
bg = pygame.image.load("resources/image/bg.jpg")
bg = pygame.transform.scale(bg, (screenWidth,screenHeight))

snakeList = []
snake_length = 1

score=0

# clock 

clock = pygame.time.Clock()

# functions 

font = pygame.font.SysFont(None, 55)

def showScore(text, color,x,y):
	screenText = font.render(text,True, color)
	gameWindow.blit(screenText, (x,y))

def drawSnake(snakeList):
	for x,y in snakeList:
		gameWindow.blit(block, (x,y))

# game loop 

while not exitGame:


	if gameOver:
		# gameWindow.fill(white)
		showScore("Game Over! please enter to continue", red, screenWidth/6, screenHeight/3)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exitGame= True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					gameOver=False
					x = 45
					y = 45
					size = 40
					FPS=30
					velocity_x = 0
					velocity_y = 0
					speed = 5
					food_x = random.randint(0, screenWidth-200)
					food_y = random.randint(0,screenHeight-200)
					snakeList = []
					snake_length = 1
					score=0
					continue
	else:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exitGame= True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					velocity_x=speed
					velocity_y=0
				if event.key == pygame.K_LEFT:
					velocity_x=-speed
					velocity_y=0
				if event.key == pygame.K_UP:
					velocity_y=-speed
					velocity_x=0
				if event.key == pygame.K_DOWN:
					velocity_y=speed
					velocity_x =0 
		y += velocity_y
		x += velocity_x

		if abs(x-food_x) < 22 and abs(y-food_y) < 22:
			score+=5
			food_x = random.randint(0, screenWidth-200)
			food_y = random.randint(0,screenHeight-200)
			snake_length +=5
			if score > int(highScore):
				highScore =score
		


		gameWindow.blit(bg,(0,0))
		# showScore(f"Score : {score*5}",red, 5,5)
		if score !=0:
			if highScore != 0 :
				pygame.display.set_caption(f"Snake Game |  Score : {score} | High Score : {highScore}")
			pygame.display.set_caption(f"Snake Game |  Score : {score}")
		head = []
		head.append(x)
		head.append(y)

		if x<0 or x>screenWidth or y <0 or y>screenHeight:
			gameOver=True
		if head in snakeList[:-1]:
			gameOver=True

		snakeList.append(head)
		if len(snakeList) > snake_length:
			del snakeList[0]
		gameWindow.blit(apple, (food_x,food_y))
		drawSnake(snakeList)
	
	pygame.display.update()
	clock.tick(FPS)
pygame.quit()
quit()