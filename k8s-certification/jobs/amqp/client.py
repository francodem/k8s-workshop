import pika
import argparse

def create_queue(queue_name):
    """Create a queue with the specified name on the RabbitMQ server.

    Args:
        queue_name (str): The name of the queue to be created.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    print(f"Queue '{queue_name}' created successfully.")
    connection.close()
    
def publish_message(queue_name, message):
    """Publish a message to a specified queue on the RabbitMQ server.

    Args:
        queue_name (str): The name of the queue to send the message to.
        message (str): The message to be sent.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
    )
    print(f"Message sent to queue '{queue_name}': {message}")
    connection.close()

def consume_one_message(queue_name):
    """Consume one message from a specified queue on the RabbitMQ server and then stop consuming.

    Args:
        queue_name (str): The name of the queue from which to consume the message.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    def callback(ch, method, properties, body):
        print(f"Received: {body.decode()}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.stop_consuming()
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
    print(f"Waiting for a message in queue '{queue_name}'.")
    channel.start_consuming()
    connection.close()

def main():
    """Main function to handle command line arguments for managing RabbitMQ queues."""
    parser = argparse.ArgumentParser(description="RabbitMQ Client to manage queues")
    parser.add_argument('-func', choices=['create', 'publish', 'consume'], required=True, help='Function to perform')
    parser.add_argument('-q', '--queue', required=True, help='Queue name')
    parser.add_argument('-m', '--message', help='Message to send to queue, required for publish function')

    args = parser.parse_args()

    if args.func == 'create':
        create_queue(args.queue)
    elif args.func == 'publish':
        if args.message:
            publish_message(args.queue, args.message)
        else:
            parser.error("The message is required for the publish function.")
    elif args.func == 'consume':
        consume_one_message(args.queue)

if __name__ == "__main__":
    main()
