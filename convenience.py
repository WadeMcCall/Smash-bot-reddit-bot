import datetime
import json

redditTimeZoneDiff = -8

def now():
	return datetime.datetime.now()
	
def get_date(submission):
	time = submission.created
	return datetime.datetime.fromtimestamp(time) + datetime.timedelta(hours=redditTimeZoneDiff)
	
def safeprint(s):
	try:
		print(s)
	except:
		print(s.encode('utf8'))
		
def safeprintdict(obj):
    safeprint(json.dumps(obj, indent = 4))

def mysplit(s):
     words = []
     inword = 0
     for c in s:
         if c in " \r\n\t": # whitespace
             inword = 0
         elif not inword:
             words = words + [c]
             inword = 1
         else:
             words[-1] = words[-1] + c
     return words