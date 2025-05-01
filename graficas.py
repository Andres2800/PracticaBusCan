import matplotlib.pyplot as plt  # type: ignore

def leer_paquetes_can(archivo):
    lista_0D = []
    lista_0C = []
    lista_46 = []
    tiempos_0D = []
    tiempos_0C = []

    with open(archivo, 'r') as f:
        for linea in f:
            try:
                # Extraer timestamp entre paréntesis
                if '(' not in linea or ')' not in linea:
                    continue
                timestamp = float(linea[linea.find('(')+1 : linea.find(')')])

                partes = linea.strip().split()
                if len(partes) < 3:
                    continue

                id_y_datos = partes[2].split('#')
                if len(id_y_datos) != 2:
                    continue

                id_can, datos = id_y_datos
                
                if id_can.upper() != '7E8':
                    continue

                if len(datos) < 12:
                    continue

                primeros_cuatro_bytes = datos[6:14]
                byte_5_6 = datos[4:6]

                if byte_5_6.upper() == '0D':
                    lista_0D.append(primeros_cuatro_bytes)
                    tiempos_0D.append(timestamp)
                elif byte_5_6.upper() == '0C':
                    lista_0C.append(primeros_cuatro_bytes)
                    tiempos_0C.append(timestamp)
                elif byte_5_6.upper() == '46':
                    lista_46.append(primeros_cuatro_bytes)
                # Si quieres guardar tiempos_46 también, puedes agregarlo aquí

            except Exception as e:
                print(f"Error procesando línea: {linea}\n{e}")

    return lista_0D, tiempos_0D, lista_0C, tiempos_0C, lista_46

# Uso del código
archivo_log = "salida.log"
lista_0D, tiempos_0D, lista_0C, tiempos_0C, lista_46 = leer_paquetes_can(archivo_log)

velocidades = []
RPMs = []

for i in lista_0D:
    A = int(i[0:2], 16)
    velocidades.append(A)

for i in lista_0C:
    A = int(i[0:2], 16)
    B = int(i[2:4], 16)
    RPMs.append((256 * A + B) / 4)

# Graficar con marcas de tiempo
plt.figure(figsize=(10, 8))

# Subplot para la velocidad
plt.subplot(2, 1, 1)
plt.plot(tiempos_0D, velocidades, label='Velocidad', color='blue')
plt.title('Velocidad')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (km/h)')
plt.legend()
plt.grid()

# Subplot para las RPM
plt.subplot(2, 1, 2)
plt.plot(tiempos_0C, RPMs, label='RPM', color='red')
plt.title('Revoluciones por Minuto')
plt.xlabel('Tiempo (s)')
plt.ylabel('RPM')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
