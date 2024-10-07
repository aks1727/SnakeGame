if x<0 or x>screenWidth or y <0 or y>screenHeight:
			gameOver=True
		if head in snakeList[:-1]:
			gameOver=True