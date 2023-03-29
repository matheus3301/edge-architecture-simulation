import uuid

from smartwatch import Smartwatch


device = Smartwatch(
    str(uuid.uuid4()),
    0.001,
    'data.csv',
    'localhost',
    5672,
    'guest',
    'guest',
    'smartwatch_sensor_data'
)