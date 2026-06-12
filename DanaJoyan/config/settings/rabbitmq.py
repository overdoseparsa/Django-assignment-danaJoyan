from config.env import env


RABBITMQ_URL = env('RABBITMQ_URL',default = "amqp://admin:admin123@localhost:5672/")
QUEUE_NAME = env("QUEUE_NAME",default="test-queue")

