import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='userlog')

def callback(ch, method, properties, body):
    print(" [x] %s" % body.decode('utf-8'))

channel.basic_consume(callback, queue='userlog', no_ack=True)

print(' [*] Waiting for logging messages. To exit press CTRL+C')
channel.start_consuming()