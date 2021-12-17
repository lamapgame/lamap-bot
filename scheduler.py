from pony.orm import db_session
from config import DB_URL
from apscheduler.schedulers.blocking import BlockingScheduler
import database
sched = BlockingScheduler()

database.db.bind('postgres', DB_URL)
database.db.generate_mapping(create_tables=True)


@sched.scheduled_job('cron', day_of_week='sun', hour=10)
@db_session
def share_nkap():
    database.db.execute(
        """
        update userdb
        set nkap = 25000
        CASE
            WHEN nkap < 0 THEN nkap + 25000
            when nkap < 25000 then 25000
            else nkap
            end 
        where nkap < 25000 
        and id not in (
            select id from userdb u
            where games_played < 10
        ) and verified = true
        """
    )
    print('-ADMIN- MONEY DROP')


sched.start()
