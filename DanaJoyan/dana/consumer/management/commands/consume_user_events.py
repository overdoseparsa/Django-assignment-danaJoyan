import json
import pika
from django.core.management.base import BaseCommand
from django.db import transaction, close_old_connections
from django.conf import settings
from dana.users.models import UserApp


class Command(BaseCommand):
    help = "Starts the RabbitMQ consumer"

    def handle(self, *args, **kwargs):
        self.stdout.write("Connecting to RabbitMQ...")

        params = pika.URLParameters(settings.RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.queue_declare(queue=settings.QUEUE_NAME, durable=True)
        channel.basic_qos(prefetch_count=1)

        def callback(ch, method, properties, body):
            self.stdout.write(f"RAW MESSAGE: {body!r}")
            close_old_connections()

            try:
                data = json.loads(body.decode())
                self.stdout.write(f"PARSED DATA: {data}")

                event_type = data.get("event_type")
                self.stdout.write(f"EVENT TYPE: {event_type}")

                if event_type == "user.created":
                    with transaction.atomic():
                        obj, created = UserApp.objects.update_or_create(
                            user_id=data["user_id"],
                            defaults={
                                "username": data["username"],
                                "user_email": data["user_email"],
                                "role": data.get("user_role", "USER"),
                            },
                        )
                    self.stdout.write(
                        f"Processed user {data['user_id']} created={created}"
                    )
                else:
                    self.stderr.write("Skipping unknown event_type")

                ch.basic_ack(delivery_tag=method.delivery_tag)

            except Exception as e:
                self.stderr.write(f"ERROR processing message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        channel.basic_consume(
            queue=settings.QUEUE_NAME,
            on_message_callback=callback,
        )

        self.stdout.write("Waiting for messages...")
        channel.start_consuming()
