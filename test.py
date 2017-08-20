import praw
import convenience
import datetime
import time
import pysmash
import pySmashParser
import pickle
from operator import itemgetter

def main():
	smash = pysmash.SmashGG()
	stats = []
	#command = "Mang0 is much better than HBOX see!!! !melee (low tier city 5) lucky if you dont agree with me you all suck!!"
	#list1 = pySmashParser.getCommand(command)
	#ret = pySmashParser.parsePlayers(list1[0], 'melee', stats)
	#players = ret[0]
	#stats = ret[1]
	#print(needsReParsing(players))
	##player_sets = smash.tournament_show_player_sets('super-smash-con-2017', 'mang0', 'melee-singles')
	#player = pySmashParser.getPlayerFromListByTag(list1[1], players)
	#
	#message = "{0}:\n\nTotal games won: {1}  \nTotal games lost: {2}  \n Players Defeated:\n\n&nbsp;&nbsp;&nbsp;&nbsp; {3}  \n Lost To:\n\n&nbsp;&nbsp;&nbsp;&nbsp; {4}  \n Final Placing: {5}  \n Seed: {6}  \n\n ------  \n *I am a bot! my info comes from [smash.gg](https://smash.gg/) (unofficial) for bug reporting or suggestions, please message /u/gronkey*".format(player['tag'], player['Games won'], player['Games lost'],'  \n&nbsp;&nbsp;&nbsp;&nbsp;'.join(player['won against']) ,'  \n&nbsp;&nbsp;&nbsp;&nbsp;'.join(player['lost to']), player['final_placement'], player['seed'])
	#convenience.safeprint(message)
	##playerStats = pySmashParser.findDictFromList(stats, list1[1])
	##playerStats = playerStats.get('melee')
	##convenience.safeprintdict(playerStats)
	#
	#command = "Mang0 is much better than HBOX see!!! !wiiu (low tier city 5) zero if you dont agree with me you all suck!!"
	#list1 = pySmashParser.getCommand(command)
	#ret = pySmashParser.parsePlayers(list1[0], 'wiiu', stats)
	#players = ret[0]
	#stats = ret[1]
	#print(needsReParsing(players))
	#print(list1[1])
	##player_sets = smash.tournament_show_player_sets('super-smash-con-2017', 'mang0', 'melee-singles')
	#player = pySmashParser.getPlayerFromListByTag(list1[1], players)
	#
	#message = "{0}:\n\nTotal games won: {1}  \nTotal games lost: {2}  \n Players Defeated:\n\n&nbsp;&nbsp;&nbsp;&nbsp; {3}  \n Lost To:\n\n&nbsp;&nbsp;&nbsp;&nbsp; {4}  \n Final Placing: {5}  \n Seed: {6}  \n\n ------  \n *I am a bot! my info comes from [smash.gg](https://smash.gg/) (unofficial) for bug reporting or suggestions, please message /u/gronkey*".format(player['tag'], player['Games won'], player['Games lost'],'  \n&nbsp;&nbsp;&nbsp;&nbsp;'.join(player['won against']) ,'  \n&nbsp;&nbsp;&nbsp;&nbsp;'.join(player['lost to']), player['final_placement'], player['seed'])
	#convenience.safeprint(message)
	
	#convenience.safeprintdict(playerStats)
	
	#print(list1[1])
	try:
		stats = pickle.load(open("stats.p","rb"))				#load previously saved stats, if any.
	except EOFError:
		stats = []	
		
	#playerStats = pySmashParser.findDictFromList(stats, 'Armada')
	#playerStats = playerStats.get('stats')
	#print(list1[0])
	#convenience.safeprintdict(playerStats)
	sortedStats = sortStats(stats, 'melee')						
	message = "Top 10:\n\n1: {0} - {10}   \n2: {1} - {11}   \n3: {2} - {12}   \n4: {3} - {13}   \n5: {4} - {14}   \n6: {5} - {15}   \n7: {6} - {16}   \n8: {7} - {17}   \n9: {8} - {18}   \n10: {9} - {19}".format(sortedStats[0]['stats']['tag'], sortedStats[1]['stats']['tag'], sortedStats[2]['stats']['tag'], sortedStats[3]['stats']['tag'],sortedStats[4]['stats']['tag'],sortedStats[5]['stats']['tag'],sortedStats[6]['stats']['tag'],sortedStats[7]['stats']['tag'],sortedStats[8]['stats']['tag'],sortedStats[9]['stats']['tag'], int(sortedStats[0]['stats']['elo']),int(sortedStats[1]['stats']['elo']),int(sortedStats[2]['stats']['elo']),int(sortedStats[3]['stats']['elo']),int(sortedStats[4]['stats']['elo']),int(sortedStats[5]['stats']['elo']),int(sortedStats[6]['stats']['elo']),int(sortedStats[7]['stats']['elo']),int(sortedStats[8]['stats']['elo']),int(sortedStats[9]['stats']['elo']))

	convenience.safeprint(message)
	#print(ranking)
	

def needsReParsing(tournament):
	if 'winner' in tournament:
		return 0
	else:
		return 1

		

def sortStats(stats, type):
	legalStats = []
	for stat in stats:
		if(str(stat['type']) == str(type)):
			legalStats.append(stat)
	
	return sorted(legalStats, key=lambda k: k['stats']['elo'], reverse=True)

def getRanking(stats, playerName, type):
	legalStats = []
	for stat in stats:
		if(str(stat['type']) == str(type)):
			legalStats.append(stat)
	
	legalStats = sorted(legalStats, key=lambda k: k['stats']['elo'], reverse=True) 
	return findIndexFromDict(legalStats, playerName)
	
def findIndexFromDict(lst, playerName):
	return next(index for (index, d) in enumerate(lst) if d['stats']['tag'] == playerName)
		
if __name__ == '__main__':
    main()