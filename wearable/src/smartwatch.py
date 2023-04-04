import csv
import time
import json
import pika


class Smartwatch():
    def __init__(self, unique_identifer: str,  sampling_period: int, buffer_size: int, filename: str, broker_hostname: str, broker_port: int, broker_username: str, broker_password: str, queue_name: str) -> None:
        print("[x] Booting the Smartwatch simulation")
        print(f"[x] The smartwatch got the id {unique_identifer}")

        self.__unique_identifer = unique_identifer
        self.__sampling_period = sampling_period
        self.__buffer_size = buffer_size
        self.__filename = filename
        self.__broker_hostname = broker_hostname
        self.__queue_name = queue_name

        try:
            credentials = pika.PlainCredentials(broker_username, broker_password)

            self.__connection = pika.BlockingConnection(
                pika.ConnectionParameters(self.__broker_hostname, broker_port, '/', credentials)
            )
        except Exception:
            print("[x] Unable to establish connection with RabbitMQ broker")
            quit(1)


        self.__channel = self.__connection.channel()
        self.__channel.queue_declare(queue=self.__queue_name)

        print(
            f"[x] The smartwatch will start transmitting the data with a sampling time of {self.__sampling_period} seconds over a buffer with size {self.__buffer_size}"
        )

        self.__start_transmiting_data()

    def __start_transmiting_data(self) -> None:
        print("[x] Start transmitting data")
        
        accumulated_data = []
        while True:
            print(f"[x] Starting reading {self.__filename}")
            with open(self.__filename, newline='') as csvfile:
                print("[x] Opened the csv file successfully")

                spamreader = csv.DictReader(csvfile)

                for data in spamreader:
                    data = self.__transform_data(data)

                    if len(accumulated_data) == self.__buffer_size:
                        self.__send_data(accumulated_data)
                        accumulated_data = []

                    accumulated_data.append(data)                        

                    time.sleep(self.__sampling_period)

            print(f"[x] Finished reading {self.__filename}")

    def __transform_data(self, data: dict) -> dict:
        del data['SystemDate']
        del data['SystemTime']
        data['SmartwatchId'] = self.__unique_identifer
        data['Timestamp_Sensor(us)'] = time.time_ns()

        return data

    def __send_data(self, data: dict) -> None:
        # print("[x] Sending data to the broker")
        self.__channel.basic_publish(
            exchange='', routing_key=self.__queue_name, body=json.dumps(data)
        )

    def __del__(self):
        print("[x] Stopping the smartwatch")
        try:
            self.__connection.close()
        except Exception:
            pass