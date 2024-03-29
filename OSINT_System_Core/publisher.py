import pika
import pika.exceptions
import datetime
import json
import sys

class Rabbit_Publisher(object):

    """
    Class to create the publisher object and use it to broadcast the messages to all listners
    it also consists all the class level variables
    """

    #class level variables bellow

    HOST = None
    USERNAME = None
    PASSWORD = None
    EXCHANGE = None
    EXCHANGE_TYPE = 'fanout'
    ROUTING_KEY = ''
    PROPERTIES = pika.BasicProperties(content_type='application/json',delivery_mode=1)
    VIRTUAL_HOST = 'system_control'


    def __init__(self,host = '192.168.18.27',username = '',password = '',exchange=''):
        """
        Do initial connection to the rabbitmq server and create a queue
        """

        self.HOST = host
        self.USERNAME = username
        self.PASSWORD = password
        self.EXCHANGE = exchange
        self._connection = None
        try:
            credentials = pika.credentials.PlainCredentials(self.USERNAME, self.PASSWORD)
            self._connection =pika.BlockingConnection(pika.ConnectionParameters(host=self.HOST, credentials=credentials,virtual_host=self.VIRTUAL_HOST))
            if(self._connection.is_open):
                self._connection.add_on_connection_blocked_callback(self.on_connection_blocked)
                self._connection.add_on_connection_unblocked_callback(self.on_connection_open_unblocked)
                self._connection.add_callback_threadsafe(self.blocking_thread)
                self.channel = self._connection.channel()
                self.channel.exchange_declare(exchange=self.EXCHANGE, exchange_type=self.EXCHANGE_TYPE,durable=False, auto_delete=False)
                self.channel.confirm_delivery()
                #print('.....................................RabbitMq Connected To Exchange : {0}.......................'.format(self.EXCHANGE))
        except pika.exceptions.ProbableAuthenticationError as e :
            print('.....................................RabbitMq Not Connected.............................................')
            print(e)
        except Exception as e:
            print(e)

    def on_connection_blocked(self):
        print('................................Connection Blocked By RabbitMq..............................')

    def on_delivery_confirmation(self, method_frame):

        confirmation_type = method_frame.method.NAME.split('.')[1].lower()
        print(method_frame)

    def on_connection_open_unblocked(self):
        print('................................Connection Un-Blocked By RabbitMq..............................')

    def blocking_thread(self):
        print('................................In Blocking Connection Safe Thread..............................')

    def is_connected(self):
        if(self._connection is not None):
            return self._connection.is_open
        return False

    def publish(self,message,routing_key = '',):
        try:
            if(self.is_connected()):
                val = self.channel.basic_publish(exchange=self.EXCHANGE,
                                      routing_key=self.ROUTING_KEY,
                                      body=json.dumps(message),
                                      properties=self.PROPERTIES,
                                      mandatory=True
                                           )
                #print(self.channel.basic_get(self.EXCHANGE))
                return True

        except pika.exceptions.UnroutableError as e:
            print('Message is returned, it says ', e)

        except pika.exceptions.ChannelClosed as e:
            print(e)
        except pika.exceptions.ConnectionClosed as e:
            print(e)
        except pika.exceptions.ConnectionOpenAborted as e:
            print(e)
        except pika.exceptions.ChannelError as e:
            print(e)

        except Exception as e:
            print(e)

        return False





SERVER_NAME = 'OCS'

def publish(message,module_name =__name__,message_type='info',**kwargs):
    pub = Rabbit_Publisher(username='ocs', password='rapidev', exchange='control_exchange')
    #publish({'server_name': 'OCS', 'module_name': __name__, 'messege_type': 'info','arguments':{'name':'awais'},'messege':'this is the messege'})
    pub.publish({'server_name': SERVER_NAME, 'module_name':module_name, 'message_type': message_type,'arguments':kwargs,'messege':message})


#def publish_control(message,module_name = __name__):
#    publish({'server_name': SERVER_NAME, 'module_name': module_name, 'messege_type': 'control','arguments':{},'messege':message})


#if __name__ == '__main__':
#    pub = Rabbit_Publisher(username='ocs',password='rapidev',exchange='control_exchange')
#    data = {'server_name':'OCS','node_id':1,'messege_type':'control, awais'}
#    print(pub.publish(data))