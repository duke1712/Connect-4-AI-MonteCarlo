
# First Create a Game object
# Call the create_game function to create the game
# create_game calls the create_board
# from Monte_Carlo import *
from random import choice

class Game:
	def __init__(self):
		self.board = []
		self.rows = 0
		self.columns = 0
		self.turn = 0
		self.cells = []		#Stores the unwinnable cells
		self.hc = 0
		self.player1AI = 100	#Stored the number of random sequences for player 1
		self.player2AI = 100	#Stored the number of random sequences for player 1

	def create_game(self, player1AI, player2AI):
		# Uncomment the 2 below lines, to play with human players
		self.rows = int(5)  #raw_input("Enter number of rows\n"))
		self.columns = int(5)  #raw_input("Enter number of columns\n"))
		self.player1AI = player1AI
		self.player2AI = player2AI
		cols = []
		cells = []
		for i in range(self.columns):
			cols.append(self.rows)  #raw_input("Enter number of rows for column "+str(i)+"\n"))
		#Uncomment the below lines to enter input from the user.
		cells.append('A2')  # raw_input("Enter first row/column as 'B3' for which you dont want a winnable cell\n"))
		cells.append('C4')  # raw_input("Enter secound row/column as 'B3' for which you dont want a winnable cell\n"))

		for i in xrange(2):
			col = ord(cells[i][0])-65
			row = cells[i][1:]
			self.cells.append((row, col))

		return self.create_board(cols)

	# Function to create board
	# Here '#' means a not playable cell
	# '_' means and empty cell
	def create_board(self, cols):
		self.board = [['_' for i in range(self.columns)] for x in range(self.rows)]
		for i in range(0, self.columns):
			for j in range(0, self.rows-int(cols[i])):
				self.board[j][i] = "#"
		return self.board

	# Function to print the board
	def print_board(self):
		for i in range(0,self.columns):
			print "  "+str(i)+" ",
		print("")
		for i in self.board:
			print i

	# Function  to insert the coin to the given column
	def insert_coin(self, board, coin, col):
		flag = 1
		for i in reversed(range(0, len(board))):
			if board[i][col] == '#':
				flag = 1
				break

			if board[i][col] == '_':
				flag = 0
				board[i][col] = coin
				break
		if flag == 1:
			# self.print_board()
			return False, col
		else:
			# self.print_board()
			return True, col

	# Function to ask create a moves for either player
	def generate_move(self):
		w = self.check_win(self.board)	#Checking for winner
		if w > 0:
			print("Game Ended")
		else:
			if self.turn == 0:
				cols = []
				while True:
					if self.hc == 1:
						# Human player code
						self.print_board()
						col = raw_input("Enter column number for you turn\n")
						state = self.insert_coin(self.board, "X", int(col))
						if state:
							break
						print("Wrong Column please enter correct column!")
					else:
						# Computer player code
						col = self.get_winning_move(self.board, 'X',cols)
						if col == -1:
							col = self.get_move(self.board, 'X', self.player1AI, cols)
						print(col)
						state,pos=self.insert_coin(self.board, 'X', col)
						cols.append(pos)
						if state:
							break
			else:
				cols = []
				while True:
					# Computer code for player 2
					col = self.get_winning_move(self.board, 'O', cols)
					if col == -1:
						col = self.get_move(self.board, 'O', self.player2AI,cols)
					print(col)
					state, pos=self.insert_coin(self.board, "O", col)
					cols.append(pos)
					if state:
						break

		if self.turn == 0:
			self.turn = 1
		else:
			self.turn = 0

	# Function to return the winning move
	def get_winning_move(self, board,player,a):
		for i in range(0, self.columns):
			win = 0
			if i not in a:
				copy = self.copy_board(board)
				self.insert_coin(copy, player, i)
				win = self.check_win(copy)
			if win > 0:
				return i
		return -1

	def end_game(self, board):
		if self.has_moves(board):
			return False
		else:
			return True

	def has_moves(self, board):
		c = 0
		for i in range(0, self.columns):
			for j in range(0, self.rows):
				if board[j][i] == '_':
					c += 1
					break
		if c == 0:
			return False
		else:
			return True

	def check_win(self, board):
		win = [
			self.win_horizontally(board),
			self.win_vertically(board),
			self.win_bottom_right_diagonally(board),
			self.win_up_right_diagonally(board),
			self.win_bottom_left_diagonally(board),
			self.win_up_left_diagonally(board)]
		# print win
		if sum(win) > 0:
			return sum(win)
		# elif 2 in win:
		# 	return 2
		else:
			return 0

	def win_horizontally(self, board):
		count = 0
		for i in range(0, self.rows):
			temp = board[i][0]
			count = 0
			for j in range(0, self.columns):
				if (i, j) in self.cells:
					count = 0
					continue
				if count == 4:
					return 0
				if board[i][j] == '#':
					count = 0
					continue
				if board[i][j] == temp and temp != '_':
					count += 1
					if count == 4:
						return 1 if temp == 'X' else 2
				else:
					temp = board[i][j]
					if temp != '_':
						count = 1
					if temp == '_':
						count = 0
		return 0

	def win_vertically(self, board):
		count = 0
		for i in range(0, self.columns):
			temp = board[0][i]
			count = 0
			for j in range(0, self.rows):
				if (i, j) in self.cells:
					count = 0
					continue
				if count == 4:
					return 0
				if board[j][i] == '#':
					count = 0

					continue
				if board[j][i] == temp and temp != '_':
					count += 1
					if count == 4:
						return 1 if temp == 'X' else 2
				else:
					temp = board[j][i]
					if temp != '_':
						count = 1
					if temp == '_':
						count = 0
		return 0

	def win_bottom_right_diagonally(self, board): #\
		count = 0
		for i in range(0, self.columns - 3):
			c = 0
			temp = board[i][0]
			count = 0
			for j in range(i, self.rows):
				if (i, j) in self.cells:
					count = 0
					c += 1
					continue
				if count == 4:
					return 0
				if board[j][c] == '#':
					count = 0
					continue
				if board[j][c] == temp and temp != '_':
					count += 1
					if count == 4:
						return 1 if temp == 'X' else 2
				else:
					temp = board[j][c]
					if temp != '_':
						count = 1
					if temp == '_':
						count = 0
				c += 1
		return 0

	def win_up_right_diagonally(self, board): #\
		count = 0
		for i in range(0, self.columns - 3):
			c = 0
			temp = board[i][0]
			count=0
			for j in range(i, self.rows):
				if (i, j) in self.cells:
					count = 0
					c += 1
				if c == self.columns:
					break
				if count == 4:
					return 0
				if board[c][j] == '#':
					count = 0
					continue
				if board[c][j] == temp and temp != '_':
					count += 1
					if count == 4:
						return 1 if temp == 'X' else 2
				else:
					temp = board[c][j]
					if temp != '_':
						count = 1
					if temp == '_':
						count = 0
				c += 1
		return 0

	def win_bottom_left_diagonally(self, board): # /
		count = 0
		for i in range(3, self.rows):
			c = 0
			temp = board[i][0]
			count = 0
			for j in reversed(range(0, i+1)):
				if (i, j) in self.cells:
					count = 0
					c += 1
				if count == 4:
					return 0
				if board[j][c] == '#':
					count = 0
					continue
				if board[j][c] == temp and temp != '_':
					count += 1
					if count == 4:
						return 1 if temp == 'X' else 2
				else:
					temp = board[j][c]
					if temp != '_':
						count = 1
					if temp == '_':
						count = 0
				c += 1
		return 0

	def win_up_left_diagonally(self, board): # /
		count = 0
		for i in range(0, self.rows):
			c = 0
			temp = board[i][0]
			count = 0
			for j in range(i, i+1):
				if (i, j) in self.cells:
					count = 0
					c += 1
				if c==self.columns:
					break
				if count == 4:
					return 0
				if board[c][j] == '#':
					count = 0
					continue
				if board[c][j] == temp and temp != '_':
					count += 1
					if count == 4:
						return 1 if temp == 'X' else 2
				else:
					temp = board[c][j]
					if temp != '_':
						count = 1
					if temp == '_':
						count = 0
				c += 1
		return 0

	def get_legal_moves(self, board):
		a = []
		for i in range(0,self.columns):
			f=0
			for j in range(0,self.rows):
				if board[j][i] == '_':
					a.append(i)
					break
		return a

	def get_current_player(self):
		if self.turn == 0:
			return 'X'
		else:
			return 'O'

	# Play random games
	def play_random(self, board, player, cols):
		while True:
			moves = self.get_legal_moves(board)
			for i in range(0,len(cols)):
				if cols[i] in moves:
					moves.remove(cols[i])
			try:
				state = self.insert_coin(board, player, choice(moves))
			except Exception as e:
				print e

			if self.end_game(board):
				return 0
			if state:
				player = 'X' if player == 'O' else 'X'
			w = self.check_win(board)

			if w > 0:
				return w

	# Copying board
	def copy_board(self, board):
		a = []
		for i in board:
			a.append(i[:])
		return a

	def get_move(self, board, player, move, cols):
		best = -1
		best_ration = 0
		games_per_move = move
		for move in range(0, self.columns):
			if move not in cols:
				won = 0
				lost = 0
				for j in range(0, games_per_move):
					copy = self.copy_board(board)

					state = self.insert_coin(copy, player, move)
					# Checking whether it was a successful move or not
					if not state:
						continue
					p = 1 if player == 'X' else 2
					if self.check_win(copy) == p:
						return move
					next = 'X'
					if p == 1:
						next = 'O'
					else:
						next = 'X'
					winner = self.play_random(copy, next, cols)
					if winner == 1 or winner == 2:
						if winner == p:
							won += 1
						else:
							lost += 1
				# Calculating win loss ration
				ratio = float(won)/(lost+1)
				if ratio >= best_ration or best == -1:
					best = move
					best_ration = ratio
		return best
