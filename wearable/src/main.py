import uuid

from smartwatch import Smartwatch

smartwatch_id = str(uuid.uuid4())

device = Smartwatch(
    smartwatch_id,
    0.001,
    'data.csv',
    'localhost',
    5672,
    'guest',
    'guest',
    'smartwatch_sensor_data_'+smartwatch_id
)