from django_eventstream import send_event
from Public_Data_Acquisition_Unit.mongo_models import Rabbit_Messages
def on_messege_recived(data,**kwargs):
    """
    this function is used to call or perform the appropriate action in a seperate thread on the message received

    :param data:
    :return:
    """
    if(data['message_type'] == 'info' or data['message_type'] == 'error' or data['message_type'] == 'warnning'):

        print(data)
        obj = Rabbit_Messages(message_type='message',message_data=data)
        obj.save()
        send_event('messages', 'message', data)
    elif(data['message_type'] == 'control' or data['message_type'] == 'alert'):
        print(data)
        obj = Rabbit_Messages(message_type='alert', message_data=data)
        obj.save()

        send_event('alerts', 'alert', data)
    elif(data['message_type'] == 'notification'):
        print(data)
        obj = Rabbit_Messages(message_type='notification', message_data=data)
        obj.save()

        send_event('notifications', 'notification', data)
    else:
        print(data)

        obj = Rabbit_Messages(message_type=data['message_type'], message_data=data)
        obj.save()
        send_event('messages', 'message', data)

