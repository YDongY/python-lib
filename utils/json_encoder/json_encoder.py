import decimal
import json
from datetime import datetime, date, time
from enum import Enum


class JsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(o, date):
            return o.strftime("%Y-%m-%d")
        elif isinstance(o, time):
            return o.strftime("%H:%M:%S")
        elif isinstance(o, decimal.Decimal):
            return str(o)
        elif isinstance(o, Enum):
            return str(o.value)
        else:
            return super().default(o)
