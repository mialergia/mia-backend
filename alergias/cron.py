from apscheduler.schedulers.background import BackgroundScheduler

import alergias.settings.base as settings
from users.models import User
from information.send_push_notification import send_push_notification
from alergias.strings import diary_reminder


def cron_send_drips():
    def mifunc():
        diary_suscribed_users = User.objects.filter(notificaciones__in=[2])

        send_push_notification(
            diary_suscribed_users,
            diary_reminder['title'],
            diary_reminder['body'],
        )

    cron_scheduler = BackgroundScheduler()
    cron_scheduler.add_job(
        mifunc,
        'cron',
        hour=19,
        minute=0,
        timezone=getattr(settings, 'TIME_ZONE'),
    )
    cron_scheduler.start()
