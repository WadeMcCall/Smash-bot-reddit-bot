import praw
import convenience
import datetime
import time
import pysmash
import pySmashParser

def main():
	smash = pysmash.SmashGG()
	command = "Mang0 is much better than HBOX see!!! !pm (Low Tier City 5) ThundeRzReiGN if you dont agree with me you all suck!!"
	list1 = pySmashParser.getCommand(command)
	players = pySmashParser.parsePlayers(list1[0], 'pm')
	print(needsReParsing(players))
	print(list1[1])
	player = pySmashParser.getPlayerFromListByTag(list1[1], players)
	
	message = "{0}:\n\nTotal games won: {1}  \nTotal games lost: {2}  \n Players Defeated:\n\n&nbsp;&nbsp;&nbsp;&nbsp; {3}  \n Lost To:\n\n&nbsp;&nbsp;&nbsp;&nbsp; {4}  \n Final Placing: {5}  \n Seed: {6}  \n\n ------  \n *I am a bot! my info comes from [smash.gg](https://smash.gg/) (unofficial) for bug reporting or suggestions, please message /u/gronkey*".format(player['tag'], player['Games won'], player['Games lost'],'  \n&nbsp;&nbsp;&nbsp;&nbsp;'.join(player['won against']) ,'  \n&nbsp;&nbsp;&nbsp;&nbsp;'.join(player['lost to']), player['final_placement'], player['seed'])
	convenience.safeprint(message)

def needsReParsing(tournament):
	if 'winner' in tournament:
		return 0
	else:
		return 1
		
if __name__ == '__main__':
    main()