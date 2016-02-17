__author__ = 'Daniel Puschmann'

from rabbitmq import RabbitMQ
import time


def hello_IoT_world():
    # establish connection
    host = "131.227.92.55"
    port = 8007
    rabbitmqconnection, rabbitmqchannel = RabbitMQ.establishConnection(host, port)

    # declare exchange
    exchange = 'Social_data'
    topic1 = 'Aarhus'
    topic2 = 'Aarhus.Traffic.SensorID002'
    RabbitMQ.declareExchange(rabbitmqchannel, exchange, _type="topic")

    json = make_message()
    RabbitMQ.sendMessage(json, rabbitmqchannel, exchange, topic1)
    time.sleep(10)

if __name__ == '__main__':
    hello_IoT_world()