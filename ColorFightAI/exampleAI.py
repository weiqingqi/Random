# You need to import colorfight for all the APIs
import colorfight
import random

if __name__ == '__main__':
	# Instantiate a Game object.
	g = colorfight.Game()
	# You need to join the game using JoinGame(). 'MyAI' is the name of your
	# AI, you can change that to anything you want. This function will generate
	# a token file in the folder which preserves your identity so that you can
	# stop your AI and continue from the last time you quit. 
	# If there's a token and the token is valid, JoinGame() will continue. If
	# not, you will join as a new player.
	if g.JoinGame('MYAI'):
		# Put you logic in a while True loop so it will run forever until you 
		# manually stop the game
		while True:
				g.Refresh()
			# Use a nested for loop to iterate through the cells on the map
				for x in range(g.width):
					for y in range(g.height):
						# Get a cell
						c = g.GetCell(x,y)
						# If the cell I got is mine
						if c.owner == g.uid:
							# Pick a direction based on current cell 
							d = [(-1,0),(0,-1), (1, 0),(0,1)]
							empty = False
							goldcount = g.gold
							# check if there is an empty cell near
							for i in range(8):
								cc = g.GetCell(x+d[random.choice([0,1,2,3])][0], y+d[random.choice([0,1,2,3])][1])
								if cc != None:
									if cc.owner == None:
										out = d[i]
										empty = True
										#if there is a empty cell set out to it and break out of the look immediately
										break 
							# check if its ready to build a base
							Readyforbase = False

							#if there is enough gold, stop when there are enough base
							if (goldcount >= 60) and (g.baseNum < 3):
								e = ([(1,1) ,(0,1), (1,-1), (1, 0), (-1,-1), (0,-1), (1,-1), (-1,1), (-1,0)])
								for i in range(8):
									cc = g.GetCell(x+e[i][0], y+e[i][1])
									if cc != None:
										#if there is a spot with ememy cell, break the look cause there is no use to build a base
										if cc.owner != g.uid:
											Readyforbase = True
											break
										#if there are a base build around, stop trying to build a base
										elif cc.buildType == 'base':
											Readyforbase = True
											break
								#if there are no ememy cells next, its time to build a base
								if Readyforbase == False:
									Readyforbase = True
								else:
									Readyforbase = False

							#if every condition to build a base is meet, build one
							if (Readyforbase == True) and (goldcount >= 60):
								g.BuildBase(x,y)
								continue


							#if there are  no empty cells
							if empty == False:
								for i in range(4):
									cc = g.GetCell(x+d[i][0], y+d[i][1])
									if cc != None:
										if cc.owner == g.uid:
											continue
										elif cc.owner != g.uid:
											out = d[i]
											break

							# If that cell is valid(current cell + direction could be
							# out of range) and that cell is not mine
							cc = g.GetCell(x+out[0], y+out[1])
							if cc != None:
								if cc.owner != g.uid:
									#print(cc.takeTime)
									#print(goldcount)
									# Attack the cell and print the result
									# if (True, None, None) is printed, it means attack
									# is successful, otherwise it will print the error
									# code and error message
									cc = g.GetCell(x+out[0], y+out[1])
									if cc.owner != g.uid:
										if cc.takeTime < 10:

											if g.energy >= 15 and cc.takeTime > 10:
												print(g.AttackCell(x+out[0], y+out[1], True))
											elif g.energy >= 60:
												print(g.AttackCell(x+out[0], y+out[1],True))
											else:
												print(g.AttackCell(x+out[0], y+out[1]))
											# Refresh the game, get updated game data
											g.Refresh()
									else:
										continue
								else:
									continue
	else:
		print("Failed to join the game!")
