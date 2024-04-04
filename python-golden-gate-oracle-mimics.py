import random
from datetime import datetime, timedelta
import os
import time
import secrets  # Import secrets module

DIR_GG_EVENTS = "./sync/test"  # Reemplaza con la ruta que deseas

def generate_random_timestamp(start_date, end_date):
  """Genera un timestamp aleatorio dentro de un rango de fechas."""
  time_delta = end_date - start_date
  random_seconds = random.randrange(int(time_delta.total_seconds()))
  return start_date + timedelta(seconds=random_seconds)

def generate_xml():
  # Define a list of possible tables
  tables = ["VENTA.BOLVEN", "GENERAL.CORRIDA", "GENERAL.TRAMO_CORRIDA", "GENERAL.TARIFA_BOLETO", "VENTA.TARIFA_BOLETO"]

  # Generate the XML document
  xml = '<?xml version="1.0" encoding="UTF-8"?>\n<OracleGoldenGateFormatXML>\n'

  # Create a random number of transactions (adjust as needed)
  num_transactions = random.randint(1, 5)
  for _ in range(num_transactions):
    timestamp = generate_random_timestamp(datetime(2024, 1, 1), datetime.today()).strftime("%Y-%m-%d:%H:%M:%S.%f")
    table = random.choice(tables)
    operation_types = ["update", "delete", "insert"]
    operation = random.choice(operation_types)

    xml += f'  <transaction timestamp="{timestamp}">\n'
    xml += f'    <dbupdate table="{table}" type="{operation}">\n'

    # Add random number of columns (adjust as needed)
    num_columns = random.randint(2, 10)
    for _ in range(num_columns):
      column_name = f"column_{random.randint(1, 100)}"
      key = random.choice(["true", "false"]) if operation == "update" else None
      status = random.choice(["null", None])  # Include null values optionally
      xml += f'      <column name="{column_name}" key="{key}" status="{status}">Value {random.randint(1, 1000)}</column>\n'

    xml += '    </dbupdate>\n'
    xml += '  </transaction>\n'

  xml += '</OracleGoldenGateFormatXML>\n'
  return xml

# Ciclo de generación de archivos
sequence_number = 1 
while True:
  xml_content = generate_xml()
  filename = f"pe{str(sequence_number).zfill(9)}"
  file_path = os.path.join(DIR_GG_EVENTS, filename)
  with open(file_path, "w") as f:
    f.write(xml_content)
  sequence_number += 1
  # Espera un tiempo aleatorio entre 5 y 15 segundos
  random_wait_time = random.randint(5, 15)
  print(f"Esperando {random_wait_time} segundos antes de generar el próximo archivo...")
  time.sleep(random_wait_time)
