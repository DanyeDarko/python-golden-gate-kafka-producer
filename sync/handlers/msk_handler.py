from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging

class KafkaProductor:

    def __init__(self, bootstrap_servers, topic):

        conf = {
        'bootstrap_servers': bootstrap_servers,
        'client_id': 'python-producer',
        'security_protocol': 'PLAINTEXT'
         }
        self.producer = KafkaProducer(**conf)
        self.topic = topic



    def send_message(self,message):
        """Envia un mensaje a un topic de Kafka."""
        try:
            self.producer.send("SPDLAY1", key=b'key', value=message.encode("utf-8"))
            self.producer.flush()
            logging.info(f"Message sent successfully to topic {self.topic}")
        except KafkaError as e:
            logging.error(f"Error al enviar mensaje a Kafka {e}")

    def cerrar(self):
        self.producer.close()