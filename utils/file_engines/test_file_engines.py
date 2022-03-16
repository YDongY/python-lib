import unittest
from file_engines import Csv, Xlsx


class TestFileEngines(unittest.TestCase):
    def setUp(self) -> None:
        self.data_list = [(1, 2, 3, 4), (1, 2, 3, 4), (1, 2, 3, 4)]
        self.header = ["a", "b", "c", "d"]
        self.csv_file = "/tmp/file/test.csv"
        self.xlsx_file = "/tmp/file/test.xlsx"

    def test_csv(self):
        Csv().writer(self.csv_file, self.data_list, header=self.header)

    def test_xlsx(self):
        Xlsx().writer(self.xlsx_file, self.data_list, header=self.header)


if __name__ == '__main__':
    unittest.main()
