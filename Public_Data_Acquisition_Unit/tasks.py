from celery.task import task
from celery.utils.log import get_task_logger
from celery.task import periodic_task
from celery.schedules import crontab
from OSINT_System_Core.publisher import publish
from Public_Data_Acquisition_Unit.acquistion_manager import *
acq = Acquistion_Manager()


@task(name="sum_two_numbers_new")
def data_acquistion_manager_task(**kwargs):
    print(kwargs)


@periodic_task(run_every=(crontab()),name='periodic_interval_targets_task')
def periodic_interval_targets_task():

    acq.target_polling()
    publish({'server_name': 'OCS', 'node_id': 1, 'messege_type': 'celery worker'})
    #print('..............................Acquistion Unit Periodic Task Executed..........................')



