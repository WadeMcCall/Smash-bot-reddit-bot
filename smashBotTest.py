import praw
import convenience
import datetime
import time
import pySmashParser

def main():
	reddit = praw.Reddit(user_agent='SmashGGBot v0.2(by /u/gronkey)',
					client_id='m12jp9GObEKxmw',
					client_secret='QnTR0Gp7thjTOIWMuTcFMznPAJU',
					username='botTestThrowaway1234',
					password=')OKMnji9')
					
	print(reddit.user.me())
	
	subreddit = reddit.subreddit('test')
	subredditComments = subreddit.stream.comments()
	
	tournaments = []
	
	botStartDate = convenience.now()
	message = "bot started: {0} \nOnly comments after this time will be affected. \n\n".format(botStartDate)
	print(message)
	
	#**** start copy-paste for update ****#
	
	for comment in subredditComments:
		if convenience.get_date(comment) > botStartDate: 	# filters out comments from before the bot is live
			text = comment.body.lower()
			commandFound = 0
			if '!smashbot' in text: 				
				eventType = 'melee'
				commandFound = 1
			elif '!wiiu' in text:
				eventType = "wiiu"
				commandFound = 1
			elif '!pm' in text:
				eventType = 'pm'
				commandFound = 1
			elif '!64' in text:
				commandFound = 1
				eventType = '64'
				commandFound = 1
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
						tourneyDict = findTournament(tournaments, tournamentName + eventType)
						currentTournament = tourneyDict.get('tournament')
						if needsReParsing(currentTournament):
							raise Exception('parse time')
					except:
						convenience.safeprint("{0} not in cached list, or unfinished tournament".format(tournamentName))
						try:
							currentTournament = pySmashParser.parsePlayers(tournamentName, eventType)
							tournaments.append({"name": tournamentName + eventType, "tournament": currentTournament})
							convenience.safeprint ("added to list: {0}".format(tournamentName))
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
					message = "player not found!"
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
	else:
		return 1
	
if __name__ == '__main__':
    main()