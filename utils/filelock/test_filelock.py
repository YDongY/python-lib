import os
import json
import unittest
from filelock import FileLock


class TestFileLock(unittest.TestCase):
    def setUp(self) -> None:
        temp_file_dir = "/tmp/file"
        self.meta_file = os.path.join(temp_file_dir, "meta")
        self.data = {"name": "mark"}

    def test_write_file(self):
        try:
            with FileLock(self.meta_file):
                with open(self.meta_file, "w") as meta_f:
                    meta_f.write(json.dumps(self.data))
        except FileNotFoundError as e:
            print(e)

    def test_read_file(self):
        try:
            with FileLock(self.meta_file):
                with open(self.meta_file, "r") as meta_f:
                    data = json.loads(meta_f.read())
        except FileNotFoundError as e:
            print(e)
        print(data)


if __name__ == '__main__':
    unittest.main()
