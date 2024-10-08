import pygame
import random

pygame.init()

# Screen dimensions
screenWidth = 1000
screenHeight = 600

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
icon_image = pygame.image.load("resources/image/gameicon.png")

# Set the icon for the window
pygame.display.set_icon(icon_image)
# Load resources
block = pygame.image.load("resources/image/block.jpg")
block = pygame.transform.scale(block, (40, 40))  # Ensure block size is 40x40
apple = pygame.image.load("resources/image/apple.png")
apple = pygame.transform.scale(apple, (40, 40))  # Resize apple to 40x40
bg = pygame.image.load("resources/image/bg.jpg")
bg = pygame.transform.scale(bg, (screenWidth, screenHeight))

# Load background music
pygame.mixer.music.load("resources/sound/background_music.mp3")
pygame.mixer.music.play(-1)  # Loop the music infinitely

# Load sound effects
eat_sound = pygame.mixer.Sound("resources/sound/eat.mp3")
hit_sound = pygame.mixer.Sound("resources/sound/hit.mp3")
gameover_sound = pygame.mixer.Sound("resources/sound/game_over.mp3")

# Font and Clock
font = pygame.font.SysFont(None, 55)
clock = pygame.time.Clock()
highScore = "0"
baseScore = 5
last_score=0
# High Score File
with open("resources/tmp/highScore.txt", "r") as f:
    highScore = int(f.read())

class SnakeGame:
    def __init__(self):
        self.gameWindow = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption(f"Snake Game | High Score: {highScore}")
        self.exitGame = False
        self.gameOver = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.speed = 5
        self.last_score = 0  # Initialize last_score here

    def showScore(self, text, color, x, y):
        screenText = font.render(text, True, color)
        self.gameWindow.blit(screenText, (x, y))

    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.speed = 5
        self.last_score = 0  # Reset last_score when the game is reset
        self.gameOver = False

    def run(self):
        global highScore
        while not self.exitGame:
            if self.gameOver:
                pygame.mixer.music.stop()  # Stop the background music on game over
                self.gameWindow.fill(white)
                self.showScore("Game Over! Press Enter to continue", red, screenWidth / 6, screenHeight / 3)
                pygame.mixer.Sound.play(gameover_sound)  # Play game over sound
                with open("resources/tmp/highScore.txt", 'w') as f:
                    f.write(str(highScore))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exitGame = True
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.reset()
                        pygame.mixer.music.play(-1)  # Restart background music
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exitGame = True
                    self.snake.handle_keys(event)

                self.snake.move(self.speed)

                # Snake eating the food
                if abs(self.snake.x - self.food.x) < 20 and abs(self.snake.y - self.food.y) < 20:
                    pygame.mixer.Sound.play(eat_sound)  # Play food eating sound
                    self.score += baseScore
                    self.food = Food()
                    self.snake.increase_length()
                    if self.score > highScore:
                        highScore = self.score

                # Speed increase logic
                if self.score >= self.last_score + 50:  # Only increase speed if score has increased by 50 or more
                    self.speed += 1
                    self.last_score = self.score

                # Update game window
                self.gameWindow.blit(bg, (0, 0))
                self.snake.draw(self.gameWindow)
                self.gameWindow.blit(apple, (self.food.x, self.food.y))

                # Display score and high score
                pygame.display.set_caption(f"Snake Game | Score: {self.score} | High Score: {highScore}")
                
                if self.snake.is_collision():
                    pygame.mixer.Sound.play(hit_sound)  # Play hit sound
                    self.gameOver = True
            pygame.display.update()
            clock.tick(30)



class Snake:
    def __init__(self):
        self.x = 45
        self.y = 45
        self.size = 40
        self.velocity_x = 0
        self.velocity_y = 0
        self.snakeList = []
        self.snake_length = 1
        self.speed = 5

    def handle_keys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.velocity_x = self.speed
                self.velocity_y = 0
            elif event.key == pygame.K_LEFT:
                self.velocity_x = -self.speed
                self.velocity_y = 0
            elif event.key == pygame.K_UP:
                self.velocity_y = -self.speed
                self.velocity_x = 0
            elif event.key == pygame.K_DOWN:
                self.velocity_y = self.speed
                self.velocity_x = 0

    def move(self, speed):
        self.speed = speed
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.snakeList.append([self.x, self.y])
        if len(self.snakeList) > self.snake_length:
            del self.snakeList[0]

    def draw(self, window):
        for segment in self.snakeList:
            window.blit(block, (segment[0], segment[1]))

    def increase_length(self):
        self.snake_length += 5

    def is_collision(self):
        # Check for boundary collision
        if self.x < 0 or self.x > screenWidth-40 or self.y < 0 or self.y > screenHeight -40:
            return True
        # Check for self-collision
        if [self.x, self.y] in self.snakeList[:-1]:
            return True
        return False


class Food:
    def __init__(self):
        self.x = random.randint(0, (screenWidth - 200) )   # Align to grid of 40x40
        self.y = random.randint(0, (screenHeight - 200) )   # Align to grid of 40x40


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
    pygame.quit()
