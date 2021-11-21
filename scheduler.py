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
