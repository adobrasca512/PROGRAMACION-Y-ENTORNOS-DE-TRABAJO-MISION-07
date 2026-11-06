import csv

# PROYECTO HEREDADO: contiene defectos intencionados.


ARCHIVO = 'ventas.csv'

def validaciones(valores):
    if not valores:
        raise ValueError('La lista de valores está vacía.')
    #validar si son negativos
    if any(v < 0 for v in valores):
        raise ValueError('Los valores no pueden ser negativos.')
    #validar si son números
    if any(not isinstance(v, (int, float)) for v in valores):
        raise ValueError('Todos los valores deben ser números.')
    #validar que no sean decimales
    if any(isinstance(v, float) and not v.is_integer() for v in valores):
        raise ValueError('Los valores no pueden ser decimales.')
    #validar que no sean nulos
    if any(v is None for v in valores):
        raise ValueError('Los valores no pueden ser nulos.')
    
    

def estimar(valores):
    validaciones(valores)
    return sum(valores) / len(valores) * 1.1

def ejecutar():
    # Leer el archivo CSV y extraer los valores de ventas
    with open(ARCHIVO) as f:
        filas = list(csv.DictReader(f))
    ventas = [float(fila['ventas']) for fila in filas]
    print('Demanda prevista:', estimar(ventas))

if __name__ == '__main__':
    ejecutar()
