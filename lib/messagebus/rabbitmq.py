import pika

__author__ = 'Daniel Puschmann'



class RabbitMQ(object):
    # Maps existing exchanges onto routing keys
    exchangetopics = []
    exchanges = ["annotated_data", "quality", "event", "annotated_event", "aggregated_data", "wrapper_registration"]
    exchange_annotated_data = exchanges[0]
    exchange_quality = exchanges[1]
    exchange_event = exchanges[2]
    exchange_annotated_event = exchanges[3]
    exchange_aggregated_data = exchanges[4]
    exchange_wrapper_registration = exchanges[5]

    @classmethod
    def establishConnection(cls, host, port, username='guest', password='guest'):
        if host == 'localhost' and port is not None:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, heartbeat_interval=600))
        elif host == 'localhost':
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, heartbeat_interval=600))
        else:
            credentials = pika.PlainCredentials(username, password)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host, heartbeat_interval=600, port=port, credentials=credentials))
        channel = connection.channel()
        return connection, channel

    # use one exchange for each data set
    # use routing key to send to the right subscribers
    @classmethod
    def sendMessage(cls, msg, channel, exchange, routing_key):
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg)

    @classmethod
    def declareExchange(cls, channel, exchange, _type='direct'):
        # Checks if exchange exists and declares the exchange in case it has not been declared before
        if exchange not in RabbitMQ.exchangetopics:
            channel.exchange_declare(exchange=exchange, exchange_type=_type, auto_delete=True)
            # RabbitMQ.exchangetopics[exchange] = [routing_key]
            RabbitMQ.exchangetopics.append(exchange)

    @classmethod
    def deleteExchange(cls, channel, exchange):
        channel.exchange_delete(exchange=exchange, nowait=True)
        if exchange in RabbitMQ.exchangetopics:
            del RabbitMQ.exchangetopics[RabbitMQ.exchangetopics.index(exchange)]
