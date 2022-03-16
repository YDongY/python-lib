import logging
import time
from datetime import datetime

LOGGER = logging.getLogger(__name__)


class IdComponent(object):

    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.mask = (1 << length) - 1  # 组件允许使用的最大值

    def get_mask(self):
        return self.mask

    def get_length(self):
        return self.length

    def generate_long(self):
        raise NotImplementedError('IdComponent is an Abstract Class')

    def generate_string(self):
        raise NotImplementedError('IdComponent is an Abstract Class')

    def __repr__(self):
        return '(%s,%s)' % (self.name, self.length)


class ZeroComponent(IdComponent):

    def __init__(self, length):
        super(ZeroComponent, self).__init__('unused', length)

    def generate_long(self):
        return 0

    def generate_string(self):
        return '0' * self.get_length()


class SecondComponent(IdComponent):

    def __init__(self, length):
        super(SecondComponent, self).__init__('second', length)

    def generate_long(self):
        return int(time.time())

    def generate_string(self):
        return str(self.generate_long()).zfill(self.length)


class MillisecondComponent(IdComponent):

    def __init__(self, length):
        super(MillisecondComponent, self).__init__('millisecond', length)

    def generate_long(self):
        utc_now = datetime.utcnow()
        return int(utc_now.microsecond / 1000)

    def generate_string(self):
        return str(self.generate_long()).zfill(self.length)
