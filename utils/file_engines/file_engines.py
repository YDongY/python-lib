import os
import csv
import tablib
from abc import ABC


class EngineABC(ABC):
    @classmethod
    def writer(cls, file, data_list, mode="a+", **kwargs):
        raise NotImplementedError("must override process")


class Csv(EngineABC):
    @classmethod
    def writer(cls, file, data_list, mode="a+", **kwargs):
        if not os.path.exists(file) and kwargs.get("header"):
            data_list.insert(0, kwargs.get("header"))

        with open(file, mode) as f:
            csv_write = csv.writer(f, delimiter=',', quotechar='\t')
            csv_write.writerows(data_list)


class Xlsx(EngineABC):
    @classmethod
    def writer(cls, file, data_list, mode="a+", **kwargs):
        if os.path.exists(file):
            with open(file, "rb+") as f:
                data = tablib.Dataset().load(f.read())
                data.extend(data_list)
        else:
            data = tablib.Dataset(*data_list)

        if kwargs.get("header"):
            data.headers = kwargs.get("header")
        with open(file, "wb") as f:
            f.write(data.export("xlsx"))


class Html(EngineABC):
    def writer(self, file, data_list, mode="a+", **kwargs):
        pass
