import uuid
import logging
from lxml import etree
from sync.utils.logging_module import Logger
from sync.handlers.msk_handler import KafkaProductor

class ProcessTransaction:
    def __init__(self,bootstrap_servers,topic):
        self.logger = Logger()
        self.msk_handler = KafkaProductor(bootstrap_servers,topic)

      
    def send_kafka(self,message):
        self.msk_handler.send_message(message)

    def process_transaction(self, transaction_str):
        try:
            self.logger.log(logging.INFO, "Process Transaction")
            print("Process Transaction")
            transaction = etree.fromstring(transaction_str)
            timestamp = transaction.get('timestamp')
            data_batch = []

            for dbupdate in transaction.findall('dbupdate'):
                self.logger.log(logging.INFO, "Database Injection")
                dbupdate.set('timestamp', timestamp)
                dbupdate_xml_str = etree.tostring(dbupdate, encoding='unicode')
                data_batch.append({
                    'Data': bytes(dbupdate_xml_str, 'utf-8'),
                    'PartitionKey': str(uuid.uuid4())
                })
            self.logger.log(logging.INFO, "Kafka MSK-<<<<<<<<<<<<<<<<<<<<<<")
            # self.msk_handler.send_message(data_batch)

        except etree.ParseError as exception:
            error_msg = f"Se detectó un XML malformado:\n{transaction_str} \n{exception}"
            self.logger.log(logging.ERROR, error_msg)
            self.handle_malformed_xml(transaction_str)

    def handle_malformed_xml(self, xml_str):
        with open("malformed_xml.txt", "a", encoding="utf-8") as file:
            file.write(xml_str)
