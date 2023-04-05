import uuid
import os

from edgenode import EdgeNode
from random import uniform


try:
    latitude = uniform(
        float(os.environ['LATITUDE_LO']),
        float(os.environ['LATITUDE_HI'])
    )
    longitude = uniform(
        float(os.environ['LONGITUDE_LO']),
        float(os.environ['LONGITUDE_HI'])
    )
    broker_hostname = os.environ['BROKER_HOSTNAME']
    broker_port = int(os.environ['BROKER_PORT'])
    broker_username = os.environ['BROKER_USERNAME']
    broker_password = os.environ['BROKER_PASSWORD']
    queue_name = os.environ['BROKER_QUEUE_NAME']

    node_id = str(uuid.uuid4())

    raspberry = EdgeNode(
        node_id,
        latitude,
        longitude,
        broker_hostname,
        broker_port,
        broker_username,
        broker_password,
        queue_name
    )
except KeyError as e:
    print(e)
