import time
from datetime import datetime

def endofdaycheck():
	today = datetime.today()
	while True:
		check = datetime.today()
		if today.day != check.day:
			print "NEW DAY"
			return
		else:
			print "Last time check: " + datetime.strftime(check, "%I:%M %p") 
			time.sleep(600)
