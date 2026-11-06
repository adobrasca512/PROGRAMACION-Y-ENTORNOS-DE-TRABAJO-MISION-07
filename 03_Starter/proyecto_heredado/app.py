import os
import csv

# PROYECTO HEREDADO: contiene defectos intencionados.
ARCHIVO = 'ventas.csv'

def estimar(valores):
    return sum(valores) / len(valores) * 1.1

def ejecutar():
    with open(ARCHIVO) as f:
        filas = list(csv.DictReader(f))
    ventas = [float(fila['ventas']) for fila in filas]
    print('Demanda prevista:', estimar(ventas))

if __name__ == '__main__':
    ejecutar()
