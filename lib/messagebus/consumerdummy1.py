__author__ = 'Daniel Puschmann'
from rabbitmq import RabbitMQ
class consumerDummy(object):
    """
    Default listener, to test if messages are sent through the message bus.
    """
    def __init__(self, exchange, key):
        self.host = "131.227.92.55"
        self.port = 8007
        self.connection, self.channel = RabbitMQ.establishConnection(self.host, self.port)
        self.exchange = exchange
        self.routing_key = key

    def start(self):
        RabbitMQ.declareExchange(self.channel, self.exchange, _type="topic")
        queue = self.channel.queue_declare()
        queue_name = queue.method.queue
        self.channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=self.routing_key)
        self.channel.basic_consume(self.onMessage,  no_ack=True)
        self.channel.start_consuming()

    def stop(self):
        self.channel.stop_consuming()

    def onMessage(self, ch, method, properties, body):
        # print ch, method, properties
        print body

if __name__ == '__main__':
    #Listens to exchange "hello" on topic "world"
    consumer = consumerDummy('Social_data', 'Aarhus.Twitter')

    #Listens to exchange "hello" on topic "world"
    #consumer = consumerDummy('Annotated_data', 'Aarhus.Traffic.SensorID002')
    consumer.start()