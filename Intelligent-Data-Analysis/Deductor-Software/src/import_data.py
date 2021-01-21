import re

class ImportData():
    """Класс обрабатывающий файл с транзакциями"""
    
    header = []
    transactions = {}

    def __init__(self, file_name):
        self.file = file_name

    def read_file(self):
        with open(self.file, "r") as f:
            f_size = len(f.readlines())
            f.seek(0)
            for l in range(f_size):
                line = re.sub("[\\s]+", "", f.readline())
                list_line = line.split("|")
                if l == 0:
                    self.header = list_line
                else:
                    trans_num = list_line[0]
                    if trans_num not in self.transactions:
                        self.transactions.update({trans_num: [list_line[1]]})
                    else:
                        self.transactions[trans_num].append(list_line[1])

    def print_trans(self):
        for i, key in enumerate(self.transactions):
            print(f"{key}: {'; '.join(self.transactions.get(key))}")
