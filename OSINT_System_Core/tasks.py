from celery.task import task
from celery.utils.log import get_task_logger
from celery.task import periodic_task
from celery.schedules import crontab

from Public_Data_Acquisition_Unit.acquistion_manager import *


@task(name="sum_two_numbers")
def add(x, y):
    return x + y



