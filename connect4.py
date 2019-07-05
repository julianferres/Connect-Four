import numpy as np
import pygame
import sys

#Global variables
BOARD_HEIGHT = 6
BOARD_WIDTH = 7
TOP_ROW = 0
EMPTY = 0
INVALID_LOC = -1
TURN_P1 = 0
PLAYER_ONE = 1


OUT_OF_RANGE = 0
NOT_WIN = False

DISTANCE_TO_SQUARE = 5

#COLOURS
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#Font 
FONT_SIZE = 75
X_FONT = 120
Y_FONT = 10

def drop_piece(board, col, piece):
	if(not is_valid_location(board,col)):
		return INVALID_LOC

	row = get_next_open_row(board, col)
	board[row][col] = piece


def winning_move(board, piece):
	return(
		check_horizontal_win(board, piece) or
		check_vertical_win(board, piece) or
		check_pos_diagonal_win(board, piece) or
		check_neg_diagonal_win(board, piece)
		)

def check_horizontal_win(board, piece):

	for row in range(BOARD_HEIGHT):
		for col in range(BOARD_WIDTH-4+1):
			win = True
			for i in range(4):
				if(board[row][col+i]!=piece):
					win = False
			if(win):
				return win
	return NOT_WIN

def check_vertical_win(board, piece):
	for row in range(BOARD_HEIGHT-4+1):
		for col in range(BOARD_WIDTH):
			win = True
			for i in range(4):
				if(board[row+i][col]!=piece):
					win = False
			if(win):
				return win
	return NOT_WIN


def check_neg_diagonal_win(board, piece):
	#Negative slope
	for row in range(BOARD_HEIGHT-4+1):
		for col in range(BOARD_WIDTH-4+1):
			win = True
			for i in range(4):
				if(board[row+i][col+i]!=piece):
					win = False
			if(win):
				return win
	return NOT_WIN

def check_pos_diagonal_win(board, piece):
	#Positive slope
	for row in range(3,BOARD_HEIGHT):
		for col in range(BOARD_WIDTH-4+1):
			win = True
			for i in range(4):
				if(board[row-i][col+i]!=piece):
					win = False
			if(win):
				return win
	return NOT_WIN





# Board functions

def is_valid_location(board, col):
	if(col < 0 or col >= BOARD_WIDTH ): return OUT_OF_RANGE
	return board[TOP_ROW][col]== EMPTY

def get_next_open_row(board, col):
	"""Always check if is a valid location first
	Otherwise, None is returned"""

	#Travel upwards
	for i in range(BOARD_HEIGHT-1,-1,-1):
		if(board[i][col]==0):
			return i

def full_board(board):
	return EMPTY not in board[TOP_ROW]

def create_board():
	board = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
	return board


def draw_board(board):
	for col in range(BOARD_WIDTH):
		for row in range(BOARD_HEIGHT):
			pygame.draw.rect(screen, BLUE, (col*SQUARE_SIZE,(row+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

			if(board[row][col]==EMPTY):
				colour = BLACK
			elif(board[row][col]==PLAYER_ONE):
				colour = RED
			else: #Player2
				colour = YELLOW

			pygame.draw.circle(screen, colour, (int((col+0.5)*SQUARE_SIZE), int((row+1.5)*SQUARE_SIZE)), RADIUS)
			#Circle center's are in the center of each square
	pygame.display.update()

	




board = create_board()
game_over = False
turn = 0

pygame.init()

SQUARE_SIZE = 100 #pixels
width = BOARD_WIDTH* SQUARE_SIZE
height = (BOARD_HEIGHT+1)* SQUARE_SIZE #+1 to fit the piece to be dropped

size = (width, height)
RADIUS = int(SQUARE_SIZE/2 - DISTANCE_TO_SQUARE)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("liberationsans", FONT_SIZE)


# Game loop
while not game_over:

	for event in pygame.event.get():


		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			#Clean previous draw
			pygame.draw.rect(screen, BLACK, (0,0,width,SQUARE_SIZE))

			posx = event.pos[0]
			colour = RED if(turn == TURN_P1) else YELLOW


			pygame.draw.circle(screen, colour, (posx,SQUARE_SIZE//2), RADIUS)

			pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			#Ask for Player input
			posx = event.pos[0]
			col = posx//SQUARE_SIZE
			
			if(drop_piece(board, col, turn+1) == INVALID_LOC):
				print("Invalid choose")
				continue
			#Turn doesn't change

			if(winning_move(board, turn+1)):
				pygame.draw.rect(screen, BLACK, (0,0,width,SQUARE_SIZE))

				colour = RED if(turn==TURN_P1) else YELLOW
				label = myfont.render("Player {} wins!".format(turn+1), 1, colour)
				screen.blit(label, (X_FONT,Y_FONT))
				print("Player {} wins!!".format(turn+1))
				game_over = True

			print(board)
			draw_board(board)


			turn = (turn + 1)%2

			if game_over:
				pygame.time.wait(3000)


