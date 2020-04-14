from apscheduler.schedulers.blocking import BlockingScheduler
from requests import get
sched = BlockingScheduler()
from datetime import datetime

# @sched.scheduled_job('interval', minutes=1)
# def timed_job():
#     get("https://somesite.com/doTweet/")

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=12)
def scheduled_job():
    get("https://somesite.com/doTweet/")
    print('i got hit at :- ' + str(datetime.now()))

sched.start()
