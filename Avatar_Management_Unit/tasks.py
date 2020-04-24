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
