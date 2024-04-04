import re
from sync.handlers.config_handler import ConfigHandler
from sync.utils.logging_module import Logger
from sync.handlers.transaction_handler import ProcessTransaction
from sync.database.data_module import Database
import logging
import json
class FileBufferHandler:
    def __init__(self):
        self.logger = Logger()
       
        self.database = Database()
        self.buffer = {}
        self.position_cache = {}
        config = ConfigHandler()
        self.regex = config.get_value('REGEX', 'TRANSACTION')
        self.transaction_handler = ProcessTransaction("192.168.42.172:9092","SPDLAY1")

    def _get_last_position(self, file):
        if file in self.position_cache:
            return self.position_cache[file]

        position = self.database.get_last_position(file)
        return position

    def _set_last_position(self, file, position):
        self.position_cache[file] = position
        self.database.set_last_position(file, position)

    def _process_buffer(self, file):
        buffer_str = "".join(self.buffer[file])
        if re.match(self.regex, buffer_str, flags=re.DOTALL):
            self.transaction_handler.process_transaction(buffer_str)
        self.buffer[file] = []

    def _extract_transactions_from_buffer(self, file):
        buffer_str = "".join(self.buffer[file])

        print("Bufeeeeeeer to kafka -> " +buffer_str)
        message= f"File: {file}, Line: {self._get_last_position(file)}, Content: {buffer_str}"
        self.transaction_handler.send_kafka(json.dumps({'message': message}))
        transactions = re.findall(self.regex, buffer_str, flags=re.DOTALL)
        for transaction_str in transactions:
            self.transaction_handler.process_transaction(transaction_str)

        self.buffer[file] = []

    def has_buffer(self, file):
        return file in self.buffer

    def init_buffer(self, file):
        self.buffer[file] = []


    def update(self, file, last_position):
        self.logger.log(logging.INFO, f"Update Buffer for : {file}")
        with open(file, 'r', encoding="utf-8") as file_obj:
            file_obj.seek(last_position)
            for line in file_obj:
                # Skip lines starting with <?xml or <OracleGoldenGateFormatXML>
                if line.strip().startswith('<?xml') or line.strip() == '<OracleGoldenGateFormatXML>':
                    continue
    
                # Add other lines to the buffer as usual
                if line.strip() == '</transaction>':
                    self.buffer[file].append(line)
                    self._extract_transactions_from_buffer(file)
                else:
                    self.buffer[file].append(line)
    
            self._set_last_position(file, file_obj.tell())

    def get_current_position(self, file):
        return self._get_last_position(file)
