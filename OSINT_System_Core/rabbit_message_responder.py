from django_eventstream import send_event
from Public_Data_Acquisition_Unit.mongo_models import Rabbit_Messages

import os
import sys

from Public_Data_Acquisition_Unit.acquistion_manager import Timeline_Manager,Acquistion_Manager

tm = Timeline_Manager()
acq = Acquistion_Manager()


def on_messege_recived(data,**kwargs):
    """
    this function is used to call or perform the appropriate action in a seperate thread on the message received

    :param data:
    :return:
    """
    if(data['message_type'] == 'info' or data['message_type'] == 'error' or data['message_type'] == 'warnning'):

        print(data)
        obj = Rabbit_Messages(message_type='message',message_data=data,process_id=os.getpid())
        obj.save()

        if(data['server_name'].lower()=='ais'):
            on_ais_message(data)

        if (data['server_name'].lower() == 'ess'):
            on_ais_message(data)



        send_event('messages', 'message', data)
    elif(data['message_type'] == 'control' or data['message_type'] == 'alert'):
        print(data)
        obj = Rabbit_Messages(message_type='alert', message_data=data,process_id=os.getpid())
        obj.save()

        if (data['server_name'].lower() == 'ais'):
            on_ais_message(data)

        if (data['server_name'].lower() == 'ess'):
            on_ais_message(data)

        send_event('alerts', 'alert', data)
    elif(data['message_type'] == 'notification'):
        print(data)
        obj = Rabbit_Messages(message_type='notification', message_data=data,process_id=os.getpid())
        obj.save()

        if (data['server_name'].lower() == 'ais'):
            on_ais_message(data)

        if (data['server_name'].lower() == 'ess'):
            on_ais_message(data)

        send_event('notifications', 'notification', data)
    else:
        print(data)

        obj = Rabbit_Messages(message_type=data['message_type'], message_data=data,process_id=os.getpid())
        obj.save()

        if (data['server_name'].lower() == 'ais'):
            on_ais_message(data)

        if (data['server_name'].lower() == 'ess'):
            on_ais_message(data)
        send_event('messages', 'message', data)


def on_ais_message(data):
    print(data['arguments'])

    try:

        IN_CELERY_WORKER_PROCESS = sys.argv and sys.argv[0].endswith('celery') and 'worker' in sys.argv
        IN_CELERY_BEAT_PROCESS = sys.argv and sys.argv[0].endswith('celery') and 'beat' in sys.argv


        if(data['arguments']):
            if(not IN_CELERY_WORKER_PROCESS and not IN_CELERY_BEAT_PROCESS):

                if('GTR' in data['arguments']):
                    GTR_id = data['arguments']['GTR']
                    if(GTR_id is not None):
                        gtr = acq.get_gtr_by_id(GTR_id)
                        targ_obj = acq.get_dataobject_by_gtr(gtr)

                        if(targ_obj.is_recursive() and acq.get_data_response_object_by_gtr_id(gtr.id)):
                            acq.add_recursive_crawling_target(GTR_id)
                        print('.....................GOT GTR ID AIS........................')
                        tm.update_timeline_posts_by_gtr_id(gtr_id=GTR_id)
            else:
                if IN_CELERY_BEAT_PROCESS:
                    print('.......celery beat.........')
                if IN_CELERY_WORKER_PROCESS:
                    print('.......celery worker.........')
    except Exception as e:
        print(e)


def on_ess_message(data):
    pass