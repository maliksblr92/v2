from django_eventstream import send_event
from Public_Data_Acquisition_Unit.mongo_models import Rabbit_Messages

import os

from Public_Data_Acquisition_Unit.acquistion_manager import Timeline_Manager

tm = Timeline_Manager()


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
    print('...............AIS.............')
    tm.update_timeline_posts()


def on_ess_message(data):
    pass