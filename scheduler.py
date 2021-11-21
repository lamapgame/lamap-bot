from apscheduler.schedulers.blocking import BlockingScheduler
import database
sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=30)
def scheduled_job():
    database.db.execute(
        """UPDATE userdb
        SET nkap = nkap + 10000
        where nkap <= 100000 and verified = true
        """
    )
    print('This job is run every 30 seconds')


@sched.scheduled_job('cron', day_of_week='sun', hour=10)
def share_nkap():
    database.db.execute(
        """UPDATE userdb
        SET nkap = (
            CASE
            WHEN (nkap < 25000 and nkap > 0) THEN 25000
            WHEN (nkap < 0) THEN nkap + 25000
            END
        )
        where nkap <= 25000 and verified = true
        """
    )
    print('-ADMIN- MONEY DROP')


sched.start()
