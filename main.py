from datetime import datetime
import timecheck
import time
import fightcal

while True:
	today = datetime.today()
	fightcal.postcal()

	if datetime.today().day == today.day:
		timecheck.endofdaycheck()
