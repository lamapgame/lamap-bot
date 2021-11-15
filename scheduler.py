from apscheduler.schedulers.blocking import BlockingScheduler
import database
sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')


@sched.scheduled_job('cron', day_of_week='sun', hour=17)
def share_nkap():
    database.db.execute(
        """UPDATE userdb
        SET nkap = (
            CASE
            WHEN (nkap < 25000) THEN 25000
            WHEN (nkap > 25000) THEN nkap
            END
        )
        where nkap <= 25000
        """
    )
    print('time to share money')


sched.start()
