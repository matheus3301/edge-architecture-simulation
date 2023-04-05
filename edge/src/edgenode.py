import pika
import json
import time


class EdgeNode():
    def __init__(self, unique_identifier: str, latitude: float, longitude: float, broker_hostname: str, broker_port: int, broker_username: str, broker_password: str, queue_name: str) -> None:
        self.__unique_identifier = unique_identifier
        self.__latitude = latitude
        self.__longitude = longitude
        self.__broker_hostname = broker_hostname
        self.__broker_port = broker_port
        self.__queue_name = queue_name

        print("[x] Booting the edge node simulation")
        print(f"[x] The edge node got the id {self.__unique_identifier}")

        print(
            f"[x] The edge node got the latitude {self.__latitude} and longitude {self.__longitude}"
        )

        try:
            credentials = pika.PlainCredentials(
                broker_username, broker_password)

            self.__connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    self.__broker_hostname, self.__broker_port, '/', credentials)
            )

            print("[x] Connection established with RabbitMQ broker")
        except Exception:
            print("[x] Unable to establish connection with RabbitMQ broker")
            quit(1)

        channel = self.__connection.channel()
        channel.queue_declare(queue=self.__queue_name)

        print('[*] Starting listening to incoming smartwatch sensor data')
        channel.basic_consume(
            queue=self.__queue_name, on_message_callback=self.__handle_incoming_smartwatch_sensor_data, auto_ack=True
        )

        channel.start_consuming()

    def __handle_incoming_smartwatch_sensor_data(self, channel, method, properties, body) -> None:
        deserialized_body = json.loads(body)
        print(
            f"[x] New sensor data from {deserialized_body[0]['SmartwatchId']}"
        )
        self.__process_data(deserialized_body)

    def __process_data(self, data):
        time.sleep(5)
