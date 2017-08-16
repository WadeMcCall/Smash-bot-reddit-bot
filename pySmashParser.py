import pysmash
import convenience

smash = pysmash.SmashGG()
	
def parsePlayers(tournamentName):
	event = 'melee-singles'
	try:
		print(tournamentName)
		playersGG = smash.tournament_show_players(tournamentName, event)
	except:
		try:
			event = 'super-smash-bros-melee-singles'
			playersGG = smash.tournament_show_players(tournamentName, event)
		except:
			print('invalid tournament name')
			raise Exception('!')
	sets = smash.tournament_show_sets(tournamentName, event)
	for player in playersGG:
		player['Games won'] = 0
		player['Games lost'] = 0
		player['lost to'] = []
		player['won against'] = []
	
	for set in sets:
		try:
			player1 = getPlayerFromListById(int(set['entrant_1_id']), playersGG)
			player2 = getPlayerFromListById(int(set['entrant_2_id']), playersGG)
			winner = getPlayerFromListById(int(set['winner_id']), playersGG)
			loser = getPlayerFromListById(int(set['loser_id']), playersGG)
			loser['lost to'].append(winner['tag'])
			winner['won against'].append(loser['tag'])
			player1['Games won'] += set.get('entrant_1_score')
			player2['Games lost'] += set.get('entrant_1_score')
			player2['Games won'] += set.get('entrant_2_score')
			player1['Games lost'] += set.get('entrant_2_score')
		except:
			continue
		
	return playersGG
	
def getPlayerFromListById(player_id, my_list):
	return next((item for item in my_list if item['entrant_id'] == player_id), None)
	
def getPlayerFromListByTag(tag, my_list):
	tag = tag.lower()
	tag = tag.replace(" ", "")
	print(tag)
	return next((item for item in my_list if (item['tag'].lower()).replace(" ", "") == tag), None)
	
	
def getTournament(text):
	try:
		i = text.index('(')
		k = text.index (')')
		tournamentName = text[(i+1):k]
	except:
		tournamentName = None
	return tournamentName
	
def getCommand(text):
	words = convenience.mysplit(text)
	i = words.index('!smashbot')
	words = words[(i+1):]
	text = ' '.join(words)
	tournament = getTournament(text)
	command = [str("")] * 2
	try:
		text = text[text.index(tournament)+ len(tournament) + 1:]
		tournament = tournament.lower()
		tournament = tournament.replace(" ", "-")
		words = convenience.mysplit(text)
		command[0] = tournament
		command[1] = words[0] if len(words) > 0 else None
	except:
		command[1] = words[0] if len(words) > 0 else None
	return command