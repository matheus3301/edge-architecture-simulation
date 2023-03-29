import csv
import time
import json
import pika


class Smartwatch():
    def __init__(self, unique_identifer: str,  sampling_period: int, filename: str, broker_hostname: str, queue_name: str) -> None:
        print("[x] Booting the Smartwatch simulation")
        print(f"[x] The smartwatch got the id {unique_identifer}")

        self.__unique_identifer = unique_identifer
        self.__sampling_period = sampling_period
        self.__filename = filename
        self.__broker_hostname = broker_hostname
        self.__queue_name = queue_name

        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.__broker_hostname)
        )

        self.__channel = self.__connection.channel()
        self.__channel.queue_declare(queue=self.__queue_name)

        print(
            f"[x] The smartwatch will start transmitting the data on a frequency of {1/self.__sampling_period} times per second"
        )

        self.__start_transmiting_data()

    def __start_transmiting_data(self) -> None:
        print("[x] Start transmitting data")

        while True:
            with open(self.__filename, newline='') as csvfile:
                print("[x] Opened the csv file successfully")

                spamreader = csv.DictReader(csvfile)

                for data in spamreader:
                    self.__send_data(data)
                    data = self.__transform_data(data)

                    time.sleep(self.__sampling_period)

    def __transform_data(self, data: dict) -> dict:
        data['SmartwatchId'] = self.__unique_identifer
        data['SystemDate'] = None
        data['SystemTime'] = None
        data['Timestamp_Sensor(us)'] = time.time_ns()

        return data

    def __send_data(self, data: dict) -> None:
        print("[x] Sending data to the broker")
        self.__channel.basic_publish(
            exchange='', routing_key=self.__queue_name, body=json.dumps(data)
        )

    def __del__(self):
        print("[x] Stopping the smartwatch")
        self.__connection.close()
