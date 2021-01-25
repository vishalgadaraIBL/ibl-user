# amqps://ziborigv:EGUW7o28G5N_Jj80_6cIYrAjyb8ucDwV@lionfish.rmq.cloudamqp.com/ziborigv
import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user.settings")
django.setup()

from blog_user.models import User, Token
params=pika.URLParameters('amqps://ziborigv:EGUW7o28G5N_Jj80_6cIYrAjyb8ucDwV@lionfish.rmq.cloudamqp.com/ziborigv')

connection=pika.BlockingConnection(params)

channel=connection.channel()
channel.queue_declare(queue='user')

def get_token(email):
    user=User.objects.get(email=email)
    token=Token.objects.get(user=user)
    token = {'token':token.token}
    return token


def on_request(ch, method, props, body):
    body=json.loads(body)
    email = body.get('email')
    properties=props.correlation_id
    if properties == 'token_request':
        response = get_token(email)

    ch.basic_publish(exchange='',routing_key=props.reply_to,properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=json.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='user', on_message_callback=on_request, auto_ack=True)
print("USER CONSUMER STARTED.")
channel.start_consuming()
channel.close()