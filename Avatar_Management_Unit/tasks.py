from celery.task import task
from celery.utils.log import get_task_logger
from celery.task import periodic_task
from celery.schedules import crontab
from OSINT_System_Core.publisher import publish
from Avatar_Management_Unit.avatar_action_manager import Perform_Action
pa = Perform_Action()



@periodic_task(run_every=(crontab()),name='avatar_scheduled_action_task')
def avatar_scheduled_action_task():

    #pa.action_polling()
    print('.........................Avatar Action Polling.......................')
