import pika
from scoreboard import TCPClient

# tcpclienr = TCPClient(host='localhost', port=6000)

# tcpclienr.connect()



def callback(ch, method, properties, body):
    try:
        print(" [x]", body)
        # tcpclienr.send(body)
    except:
        print(" [x] Sending error")


if __name__ == '__main__':
    print(' [x] client started')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='scoreboard')
    channel.basic_consume(callback,
                          queue='scoreboard',
                          no_ack=True)

    channel.start_consuming()

