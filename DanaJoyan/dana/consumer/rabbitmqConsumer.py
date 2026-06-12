import json

import pika
from django.conf import settings
from django.db import transaction
from django.shortcuts import render

from dana.users.models import UserApp

RABBITMQ_URL = settings.RABBITMQ_URL
QUEUE_NAME = settings.QUEUE_NAME

print('RABBITMQ_URL',RABBITMQ_URL)
print('QUEUE_NAME',QUEUE_NAME)
def process_message(ch, method, properties, body):
    # change to the django

    try:
        data = json.loads(body.decode())

        event_type = data.get("event_type")
        if event_type == "user.created":
            with transaction.atomic():
                UserApp.objects.update_or_create(
                    user_id=data["user_id"],
                    defaults={
                        "username": data["username"],
                        "user_email": data["user_email"],
                        "role": data.get("user_role", "USER"),
                    },
                )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print("Error:", e)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def run_consumer():
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message)

    print(f"Listening on {QUEUE_NAME}...")
    channel.start_consuming()
