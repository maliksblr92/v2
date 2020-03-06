from django_eventstream import send_event

def on_messege_recived(data,**kwargs):
    """
    this function is used to call or perform the appropriate action in a seperate thread on the message received

    :param data:
    :return:
    """
    print(data)
    send_event('notifications', 'notification', {'GTR': '545454', 'author_account': 'ayesha.khan22'})

