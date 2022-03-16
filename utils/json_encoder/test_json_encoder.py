import datetime
import decimal
import json
import unittest
from json_encoder import JsonEncoder

from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class TestJsonEncoder(unittest.TestCase):
    def setUp(self) -> None:
        self.data = {
            "datetime": datetime.datetime(2022, 3, 16, 16, 42, 18),
            "date": datetime.date(2022, 3, 16),
            "time": datetime.time(16, 42, 18),
            "decimal": decimal.Decimal(7),
            "enum": Color.RED
        }

    def test_json_encoder(self):
        print(json.dumps(self.data, cls=JsonEncoder))


if __name__ == '__main__':
    unittest.main()
