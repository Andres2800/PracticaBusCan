from asammdf import MDF #type: ignore
import csv
import re

"""
Convertir un archivo MF4 a un archivo log
"""

# Cargar el archivo MF4
mdf = MDF('obd2/obd2/Porsche\ 991.1\ GT3RS/00000001.MF4')

# Exportar todo a un CSV
mdf.export(fmt='csv', filename='salida.csv')

# Abrir el archivo CSV
with open('salida.ChannelGroup_0.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)

    # Abrir el archivo de salida
    with open('isuzu.log', 'w') as log_file:
        for row in reader:
            timestamp = float(row['timestamps'])
            can_id = int(row['CAN_DataFrame.CAN_DataFrame.ID'])
            
            # Tomar la cadena de DataBytes y agregar las comas
            data_bytes_str = row['CAN_DataFrame.CAN_DataFrame.DataBytes']
            data_bytes_str = data_bytes_str.replace('[', '').replace(']', '').strip()
            data_bytes_list = re.split(r'\s+', data_bytes_str)  # Separar por espacios
            data_bytes = [int(byte) for byte in data_bytes_list if byte]

            # Construir la parte de datos en hexadecimal
            data_hex = ''.join(f'{byte:02X}' for byte in data_bytes)

            # Escribir línea en formato: (timestamp) vcan0 ID#data
            log_line = f"({timestamp:.6f}) vcan0 {can_id:03X}#{data_hex}\n"
            log_file.write(log_line)





