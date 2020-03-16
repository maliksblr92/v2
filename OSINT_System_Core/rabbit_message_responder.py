from django_eventstream import send_event

def on_messege_recived(data,**kwargs):
    """
    this function is used to call or perform the appropriate action in a seperate thread on the message received

    :param data:
    :return:
    """
    if(data['message_type'] == 'info' or data['message_type'] == 'error' or data['message_type'] == 'warnning'):
        send_event('messages', 'message', data)
    elif(data['message_type='] == 'control' or data['message_type'] == 'alert'):
        send_event('alerts', 'alert', data)
    elif(data['message_type='] == 'system'):
        send_event('notifications', 'notification', data)
    else:
        send_event('messages', 'message', data)

