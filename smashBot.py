import praw
import convenience
import datetime
import time
import pySmashParser

def main():
	reddit = praw.Reddit(user_agent='SmashGGBot v0.1(by /u/gronkey)',
					client_id='WkzX4VQyu6n3rg',
					client_secret='x1VpqB-VesMlg2kaasgjdfSIcAs',
					username='SmashGGBot',
					password=')OKMnji9')
					
	print(reddit.user.me())
	
	subreddit = reddit.subreddit('ssbm+smashbros')
	subredditComments = subreddit.stream.comments()
	
	tournaments = []
	tournaments.append({"name": 'super-smash-con-2017', "tournament": pySmashParser.parsePlayers('super-smash-con-2017')})
	
	botStartDate = convenience.now()
	message = "bot started: {0} \nOnly comments after this time will be affected. \n\n".format(botStartDate)
	print(message)
	
	for comment in subredditComments:
		if convenience.get_date(comment) > botStartDate: 	# filters out comments from before the bot is live
			text = comment.body.lower()
			if '!smashbot' in text: 				# filter out comments without the substring "!smashbot"
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
						tourneyDict = findTournament(tournaments, tournamentName)
						currentTournament = tourneyDict.get('tournament')
						if needsReParsing(currentTournament):
							raise Exception('parse time')
					except:
						convenience.safeprint("{0} not in cached list, or unfinished tournament".format(tournamentName))
						try:
							currentTournament = pySmashParser.parsePlayers(tournamentName)
							tournaments.append({"name": tournamentName, "tournament": currentTournament})
							convenience.safeprint ("added to list: {0}".format(tournamentName))
						except:
							message = "{0} not found!".format(command[0])
							print(message)
				try:
					player = pySmashParser.getPlayerFromListByTag(playerName, currentTournament)
					message = "{0}:\n\nTotal games won: {1}  \nTotal games lost: {2}  \n Players Defeated: {3}  \n Lost To: {4}  \n Final Placing: {5}  \n Seed: {6}  \n\n ------  \n *I am a bot! my info comes from [smash.gg](https://smash.gg/) for bug reporting or suggestions, please message /u/gronkey*".format(player['tag'], player['Games won'], player['Games lost'],', '.join(player['won against']) ,', '.join(player['lost to']), player['final_placement'], player['seed'])
					convenience.safeprint(message)
					ReplyToComment(comment, message)
				except:
					convenience.safeprint(playerName)
					message = "player not found melee singles!"
					print(message)
				
					
def ReplyToComment(comment, message):
	try:
		comment.reply(message)
	except:
		print("too many comments! Reddit API will not let you comment so frequently")

def findTournament(tournaments, tournamentName):
	return next((item for item in tournaments if item["name"] == tournamentName), None)
	
def needsReParsing(tournament):
	if 'winner' in tournament:
		return 0
	for player in tournament:
		try:
			if player["final_placement"] == 1:
				print('winner appended')
				tournament.append('winner')
				return 0
		except:
			continue
	else:
		return 1
	
if __name__ == '__main__':
    main()