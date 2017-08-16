import praw
import convenience
import datetime
import time

def main():
	reddit = praw.Reddit(user_agent='MySimpleBot v0.1(by /u/gronkey)',
					client_id='m12jp9GObEKxmw',
					client_secret='QnTR0Gp7thjTOIWMuTcFMznPAJU',
					username='botTestThrowaway1234',
					password=')OKMnji9')
	
	botStartDate = convenience.now()
	message = "bot started: {0} \nOnly comments after this time will be affected. \n\n".format(botStartDate)
	
	subreddit = reddit.subreddit('smashbros')
	printAllSubredditComments(subreddit, botStartDate)
	
def printAllSubredditComments(subreddit, commentsAfter):
	subredditComments = subreddit.stream.comments()
	for comment in subredditComments:
		if convenience.get_date(comment) > commentsAfter:
			text = comment.body
			author = comment.author
			message = "\n\n{0}:\n{1}".format(author, text)
			convenience.safeprint(message)
			

def printSubredditSubmissionsByTop(subreddit):
	for submission in subreddit.top(limit=25):
		convenience.safeprint(submission.title)

if __name__ == '__main__':
    main()