import datetime
import os

import serial.tools.list_ports
ports = serial.tools.list_ports.comports(include_links=True)

for i in ports:
        print(i.device,' ', i.description, ' ', i.product,' ', i.name, ' ', i.hwid, ' ', i.vid, ' ', i.pid)


def get_today():
    return datetime.datetime.now().strftime('%x')
def get_time():
    return datetime.datetime.now().strftime('%X')  


class Record:
    Type2Up = 2
    Type12Up = 12
    def __init__(self, code : str) -> None:
        parsed = code.split('#')
        if len(parsed) != 9:
            self.is_valid = False
            return
        self.is_valid = True
        self.code = code
        self.serial_number = parsed[8]
        self.type = int(parsed[4])
        self.timestamp = get_time()
        self.soft_date = parsed[7]

    def as_database_record(self) -> str:
        return self.serial_number + '\t' + self.code + '\t' + self.timestamp


class DataBase:
    STORAGE_PATH : str = ''
    def __init__(self, name) -> None:
        self.name = name + '.txt'
        if not os.path.isfile(self.get_path()):
            self.create_empty()
    
    def update_record(self, record : Record):
        data : dict = {}
        with open(self.get_path(), 'r') as file:
            data = file.read()
            for rec in data.split('\n'):
                rec_div = rec.split('\t')
                data[rec_div[0]] = rec
        data[record.serial_number] = record.as_database_record()
        
        with open(self.get_path(), 'w') as file:
            file.write('\n'.join(data.values()))

    def add_record(self, record : Record):
        data = ''
        with open(self.get_path(), 'r') as file:
            data = file.read()
        if data != '':
            data += '\n'
        data += record.as_database_record()
        with open(self.get_path(), 'w') as file:
            file.write(data)


    def create_empty(self):
        with open(self.get_path(), 'w') as file:
            return
    def get_path(self) -> str:
        return DataBase.STORAGE_PATH + '/' + self.name




