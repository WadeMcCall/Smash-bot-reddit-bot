import pysmash
import convenience
import elo

smash = pysmash.SmashGG()
	
def parsePlayers(tournamentName, type, stats):
	ret = []
	winner = 0
	if type == 'melee':
		events = ['melee-singles', 'super-smash-bros-melee', 'super-smash-bros-melee-singles', 'melee-singles-1']
		playersGG = []
	elif type == 'wiiu':
		events = ['wii-u-singles', 'super-smash-bros-for-wii-u-singles', 'smash-4-singles', 'super-smash-bros-for-wii-u']
		playersGG = []
	elif type == 'pm':
		events = ['pm-singles', 'project-m-singles', 'project-m-3-6-singles', 'project-m-3-02-singles']
		playersGG = []
	elif type == '64':
		events = ['64-singles', 'smash-64-singles']
		playersGG = []
	for event in events:
		try:
			print(event)
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
				winner = 1
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
	if(winner):
		stats = addStatsFromTournament(stats, sets, playersGG, tournamentName, type)
	ret.append(playersGG)
	ret.append(stats)
	return ret
	
def getPlayerFromListById(player_id, my_list):
	return next((item for item in my_list if str(item['entrant_id']) == str(player_id)), None)
	
def getPlayerFromListByTag(tag, my_list):
	tag = tag.lower()
	tag = tag.replace(" ", "")
	return next((item for item in my_list if (item['tag'].lower()).replace(" ", "") == tag), None)
	

		
def addStatsForExistingPlayer(stats, player, tournamentSize, tournamentName, type):
	playerStats = findDictFromListbyId(stats, player['tag'] + type)
	playerStats = playerStats.get('stats')
	if (player['final_placement'] == 1):
		playerStats['tournamentWins'] += 1
		playerStats['tournamentTop8s'] += 1
		playerStats['tournamentsWon'].append(tournamentName.replace("-", " ").title())
		playerStats['tournamentsTop8ed'].append(tournamentName.replace("-", " ").title())
		if(tournamentSize >= 300):
			playerStats['tournamentWinsOver300'] += 1
			playerStats['tournamentTop8sOver300'] += 1
	elif (player['final_placement'] == 7) or (player['final_placement'] == 5) or (player['final_placement'] == 4) or (player['final_placement'] == 3) or (player['final_placement'] == 2):
		playerStats['tournamentTop8s'] += 1
		playerStats['tournamentsTop8ed'].append(tournamentName.replace("-", " ").title())
		if(tournamentSize >= 300):
			playerStats['tournamentTop8sOver300'] += 1

def addStatsFromTournament(stats, sets, players, tournamentName, type):
	tournamentSize = len(players)
	print("addStatsFromTournament")
	for playert in players:
		try:
			player = playert.copy()
		except:
			continue
		try:
			playerDict = findDictFromListbyId(stats, player['tag'] + type)
			if(playerDict == None):
				raise Exception("!")
			p = playerDict.get('stats')
			if(p == None):
				raise Exception("!")
			p['Games won'] += player['Games won']
			p['Games lost'] += player['Games lost']
			addStatsForExistingPlayer(stats, player, tournamentSize, tournamentName, type)
		except:
			pStats = {}
			pStats['tag'] = player['tag']
			pStats['Games won'] = player['Games won']
			pStats['Games lost'] = player['Games lost']
			pStats['elo'] = 1500
			pStats['tournamentWins'] = 0
			pStats['tournamentTop8s'] = 0
			pStats['tournamentWinsOver300'] = 0
			pStats['tournamentTop8sOver300'] = 0
			pStats['tournamentsWon'] = []
			pStats['tournamentsTop8ed'] = []
			stats.append({"name": player['tag'], 'stats': pStats, "id": player['tag'] + type, "type": type})
			addStatsForExistingPlayer(stats, player, tournamentSize, tournamentName, type)
	for set in sets:
		for playert in players:
			try:
				player = playert.copy()
			except:
				continue
			if (str(player['entrant_id']) == str(set['entrant_1_id'])):
				try:
					opp = getPlayerFromListById(set['entrant_2_id'], players)
					if opp == None:
						continue
				except:
					continue
				oppStats = findDictFromListbyId(stats, opp['tag'] + type)
				oppStats = oppStats.get('stats')
				oppElo = oppStats['elo']
				playerStats = findDictFromListbyId(stats, player['tag'] + type)
				playerStats = playerStats.get('stats')
				playerStats['elo'] = updateElo(playerStats, set, 1, oppElo)
			elif (str(player['entrant_id']) == str(set['entrant_2_id'])):
				try:
					opp = getPlayerFromListById(set['entrant_1_id'], players)
					if opp == None:
						continue
				except:
					continue
				oppStats = findDictFromListbyId(stats, opp['tag'] + type)
				oppStats = oppStats.get('stats')
				oppElo = oppStats['elo']
				playerStats = findDictFromListbyId(stats, player['tag'] + type)
				playerStats = playerStats.get('stats')
				playerStats['elo'] = updateElo(playerStats, set, 2, oppElo)
	return stats

def updateElo(player, set, entrantNumber, oppElo):
	oppId = str()
	entrantId = str()
	score = 0
	if entrantNumber == 1:
		score = set['entrant_1_score']
		oppScore = set['entrant_2_score']
		entrantId = 'entrant_1_id'
		oppId = 'entrant_2_id'
	else:
		score = set['entrant_2_score']
		oppScore = set['entrant_1_score']
		entrantId = 'entrant_2_id'
		oppId = 'entrant_1_id'
	exp = elo.expected(player['elo'], oppElo)
	if (score == None) or (oppScore == None) or (score == -1) or (oppScore == -1):
		return player['elo']
	actual = 0
	if(score > oppScore):
		actual = 1
	return elo.elo(player['elo'], exp, actual, 96)
	
def findDictFromList(tournaments, tournamentName):
	return next((item for item in tournaments if item["name"] == tournamentName), None)

def findDictFromListbyId(tournaments, tournamentName):
	return next((item for item in tournaments if item["id"] == tournamentName), None)
	
	
def getTournament(text):
	try:
		i = text.index('(')
		k = text.index (')')
		tournamentName = text[(i+1):k]
	except:
		tournamentName = None
	return tournamentName
	
def getStatsCommand(text):
	words = convenience.mysplit(text)
	i = words.index('!stats')
	words = words[(i+1):]
	command = [str("")] *2
	command[0] = words[0]
	command[1] = words[1]
	if(command[0] == None) or (command[1] == None):
		raise Exception("!")
	return command
	
def getCommand(text):
	words = convenience.mysplit(text)
	if '!smashbot' in text.lower():
		i = words.index('!smashbot')
	if '!melee' in text.lower():
		i = words.index('!melee')
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
		tournament = tournament.replace(".", " ")
		tournament = tournament.replace("'", " ")
		tournament = tournament.replace("/", " ")
		tournament = tournament.replace("(", "")
		tournament = tournament.replace(",", "")
		tournament = tournament.replace("|", "")
		tournament = tournament.replace(":", "")
		tournament = tournament.replace("-", "")
		tournament = tournament.replace("#", "")
		tournament = tournament.replace("!", "")
		tournament = tournament.replace(";", "")
		tournament = tournament.replace("+", "")
		tournament = tournament.replace(" ", "-")
		words = convenience.mysplit(text)
		command[0] = tournament
		command[1] = words[0] if len(words) > 0 else None
	except:
		command[1] = words[0] if len(words) > 0 else None
	return command