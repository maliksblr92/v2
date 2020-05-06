from django_eventstream import send_event
def on_messege_recived(data,**kwargs):
    """
    this function is used to call or perform the appropriate action in a seperate thread on the message received

    :param data:
    :return:
    """
    if(data['message_type'] == 'info' or data['message_type'] == 'error' or data['message_type'] == 'warnning'):

        print(data)
        send_event('messages', 'message', data)
    elif(data['message_type'] == 'control' or data['message_type'] == 'alert'):
        print(data)
        send_event('alerts', 'alert', data)
    elif(data['message_type'] == 'notification'):
        print(data)
        send_event('notifications', 'notification', data)
    else:
        print(data)
        send_event('messages', 'message', data)

