import pika
from flask import g
from flask import current_app as app

def connect_queue():
    if not hasattr(g, 'rabbitmq'):
        g.rabbitmq = pika.BlockingConnection(
            pika.ConnectionParameters(app.config['RABBITMQ_HOST'])
        )
    return g.rabbitmq


def get_scroreboard_queue():
    if not hasattr(g, 'welcome_queue'):
        conn = connect_queue()
        channel = conn.channel()
        channel.queue_declare(queue='scoreboard')
        channel.queue_bind(exchange='amq.direct', queue='scoreboard')
        g.welcome_queue = channel
    return g.welcome_queue


# with app.app_context():
#     @app.teardown_appcontext
#     def close_queue(error):
#         if hasattr(g, 'rabbitmq'):
#             g.rabbitmq.close()
