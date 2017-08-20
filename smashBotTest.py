import praw
import convenience
import datetime
import time
import pySmashParser
import pickle

def main():
	reddit = praw.Reddit(user_agent='SmashGGBot v0.2(by /u/gronkey)',
					client_id='m12jp9GObEKxmw',
					client_secret='QnTR0Gp7thjTOIWMuTcFMznPAJU',
					username='botTestThrowaway1234',
					password=')OKMnji9')
					
	print(reddit.user.me())
	
	subreddit = reddit.subreddit('test')
	subredditComments = subreddit.stream.comments()
	
	#**** start copy-paste for update ****#
	
	try:
		tournaments = pickle.load(open("tournaments.p","rb"))				#load previously saved tournament, if any.
	except EOFError:
		tournaments = []
	

	try:
		stats = pickle.load(open("stats.p","rb"))				#load previously saved stats, if any.
	except EOFError:
		stats = []											
	
	botStartDate = convenience.now()
	message = "bot started: {0} \nOnly comments after this time will be affected. \n\n".format(botStartDate)
	print(message)
	
	for comment in subredditComments:
		if convenience.get_date(comment) > botStartDate: 	# filters out comments from before the bot is live
			text = comment.body.lower()
			commandFound = 0
			statsCommand = 0
			if ('!smashbot' in text) or ('!melee' in text): 				
				eventType = 'melee'
				commandFound = 1
			elif '!wiiu' in text:
				eventType = "wiiu"
				commandFound = 1
			elif '!pm' in text:
				eventType = 'pm'
				commandFound = 1
			elif '!64' in text:
				eventType = '64'
				commandFound = 1
			elif '!stats' in text:
				statsCommand = 1
			if commandFound:								# filter out comments without a command substring.
				author = comment.author
				message = "{0}:\n{1}".format(author, text)
				convenience.safeprint(message)
				try:
					command = pySmashParser.getCommand(text)	# parse the user's comment into a list containing [formatted tournament name, player name]
				except:
					continue
				tournamentName = command[0]
				playerName = command[1]
				if playerName == None:
					message = "please enter a playername! commands are given like: \"!smashbot (Super Smash Con 2017) Mang0[no spaces]"
					ReplyToComment(comment, message)
				if tournamentName == None:
					print("default tournament")
					tournamentName = 'super-smash-con-2017'
				else:
					try:
						print(tournamentName)
						tourneyDict = findDictFromList(tournaments, tournamentName + eventType)
						currentTournament = tourneyDict.get('tournament')
						if needsReParsing(currentTournament):
							raise Exception('parse time')
					except:
						convenience.safeprint("{0} not in cached list, or unfinished tournament".format(tournamentName))
						try:
							ret = pySmashParser.parsePlayers(tournamentName, eventType, stats)
							currentTournament = ret[0]
							stats = ret[1]
							tournaments.append({"name": tournamentName + eventType, "tournament": currentTournament})
							convenience.safeprint ("added to list: {0}".format(tournamentName))
							pickle.dump( tournaments, open( "tournaments.p", "wb" ) )
							pickle.dump( stats, open( "stats.p", "wb" ) )
						except:
							message = "{0} not found!".format(command[0])
							print(message)
				try:
					player = pySmashParser.getPlayerFromListByTag(playerName, currentTournament)
					message = "{0}:\n\nTotal games won: {1}  \nTotal games lost: {2}  \n Players Defeated:\n\n&nbsp;&nbsp;&nbsp;&nbsp;{3}  \n Lost To:\n\n&nbsp;&nbsp;&nbsp;&nbsp;{4}  \n Final Placing: {5}  \n Seed: {6}  \n\n ------  \n *I am a bot! my info comes from [smash.gg](https://smash.gg/) (unofficial) for bug reporting or suggestions, please message /u/gronkey*".format(player['tag'], player['Games won'], player['Games lost'],'  \n&nbsp;&nbsp;&nbsp;&nbsp;'.join(player['won against']) ,'  \n&nbsp;&nbsp;&nbsp;&nbsp;'.join(player['lost to']), player['final_placement'], player['seed'])
					convenience.safeprint(message)
					ReplyToComment(comment, message)
				except:
					convenience.safeprint(playerName)
					message = "player/tournament not found! make sure to remove spaces from player names and replace special characters with spaces in tournament names. (don t park on the grass) themoon\n\n ------  \n *I am a bot! my info comes from [smash.gg](https://smash.gg/) (unofficial) for bug reporting or suggestions, please message /u/gronkey*"
					ReplyToComment(comment, message)
			elif statsCommand:					
				author = comment.author
				message = "{0}:\n{1}".format(author, text)
				convenience.safeprint(message)
				try:
					command = pySmashParser.getStatsCommand(text)	
				except:
					continue
				oppStats = findDictFromList(stats, command[0])
				oppStats = oppStats.get(command[1])
				message = "{0}:\n\nElo score: {1}   \nTotal Tournaments Won: {2}   \nMajors won (300+ entrants): {3}   \nTotal Top 8 appearances: {4}   \nTop 8 appearances at majors: {5}   \nTournaments Won:\n\n&nbsp;&nbsp;&nbsp;&nbsp;{6}   \n Top 8s:\n\n&nbsp;&nbsp;&nbsp;&nbsp;{7}  \n\n ------  \n *I am a bot! my info comes from [smash.gg](https://smash.gg/) (unofficial) for bug reporting or suggestions, please message /u/gronkey*".format(oppStats['tag'] ,oppStats['elo'], oppStats['tournamentWins'], oppStats['tournamentWinsOver300'], oppStats['tournamentTop8s'], oppStats['tournamentTop8sOver300'], '   \n&nbsp;&nbsp;&nbsp;&nbsp;'.join(oppStats['tournamentsWon']), '   \n&nbsp;&nbsp;&nbsp;&nbsp;'.join(oppStats['tournamentsTop8ed']))
				ReplyToComment(comment, message)
				
def ReplyToComment(comment, message):
	try:
		comment.reply(message)
	except:
		print("too many comments! Reddit API will not let you comment so frequently")

def findDictFromList(tournaments, tournamentName):
	return next((item for item in tournaments if (item["name"]).lower().replace(" ", "") == tournamentName.lower().replace(" ", "")), None)
	
def needsReParsing(tournament):
	if 'winner' in tournament:
		return 0
	else:
		return 1
	
if __name__ == '__main__':
    main()