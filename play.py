from game import *

a = [80, 150, 500, 2000]
dict = {}
for j in a:
	dict[j]=[]
	for k in a:
		print "j="+str(j)+" k="+str(k)
		draw = 0
		player1_win = 0
		player2_win = 0
		for i in xrange(10):
			game = Game()
			game.create_game(j, k)
			# game.hc=int(raw_input("Want 1 computers or 2\n"))
			while True:
				game.generate_move()
				win = game.check_win(game.board)
				if game.end_game(game.board):
					draw += 1
					break
				if win % 2 != 0:
					# game.print_board()
					# print("Player 1 Won")
					player1_win += 1
					break
				elif win % 2 == 0 and win != 0:
					# game.print_board()
					# print("Player 2 Won")
					player2_win += 1
					break
		dict[j].append((k , player1_win, player2_win, draw))
		print(player1_win)
		print(player2_win)
print dict
