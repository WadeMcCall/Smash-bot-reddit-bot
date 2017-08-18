import pysmash
import convenience

smash = pysmash.SmashGG()
	
def parsePlayers(tournamentName, type):
	if type == 'melee':
		events = ['melee-singles', 'super-smash-bros-melee', 'super-smash-bros-melee-singles']
		playersGG = []
	elif type == 'wiiu':
		events = ['wii-u-singles', 'super-smash-bros-for-wii-u-singles', 'smash-4-singles']
		playersGG = []
	elif type == 'pm':
		events = ['pm-singles', 'project-m-singles', 'project-m-3-6-singles', 'project-m-3-02-singles']
		playersGG = []
	elif type == '64':
		events = ['64-singles', 'smash-64-singles', '']
		playersGG = []
	for event in events:
		try:
			print(tournamentName)
			playersGG = smash.tournament_show_players(tournamentName, event)
			break
		except:
			continue
	sets = []
	for event in events:
		try:
			sets = smash.tournament_show_sets(tournamentName, event)
		except:
			continue
	for player in playersGG:
		try:
			player['Games won'] = 0
			player['Games lost'] = 0
			player['lost to'] = []
			player['won against'] = []
			if player['final_placement'] == 1:
				print('winner found')
				playersGG.append('winner')
		except:
			continue
	
	for set in sets:
		try:
			player1 = getPlayerFromListById(int(set['entrant_1_id']), playersGG)
			player2 = getPlayerFromListById(int(set['entrant_2_id']), playersGG)
			winner = getPlayerFromListById(int(set['winner_id']), playersGG)
			loser = getPlayerFromListById(int(set['loser_id']), playersGG)
			if set.get('entrant_1_score') > set.get('entrant_2_score'):
				loserScore = set.get('entrant_2_score')
				winnerScore = set.get('entrant_1_score')
			else:
				loserScore = set.get('entrant_1_score')
				winnerScore = set.get('entrant_2_score')
			loser['lost to'].append(set.get('medium_round_text') + ": " + winner['tag'] + " " + str(loserScore) + "-" + str(winnerScore))
			winner['won against'].append(set.get('medium_round_text') + ": " + loser['tag'] + " " + str(winnerScore) + "-" + str(loserScore))
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
	if '!smashbot' in text.lower():
		i = words.index('!smashbot')
	if '!wiiu' in text.lower():
		i = words.index('!wiiu')
	if '!pm' in text.lower():
		i = words.index('!pm')
	if '!64' in text.lower():
		i = words.index('!64')
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