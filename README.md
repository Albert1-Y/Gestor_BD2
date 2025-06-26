
# Proyecto Gestor_BD2

Este proyecto es un simulador de base de datos que utiliza una estructura de disco virtual para almacenar registros. El sistema se construye usando PyQt6 para la interfaz gráfica y un enfoque orientado a objetos para la gestión de registros.

## Requisitos

- Python 3.x
- PyQt6
- Otros módulos necesarios:
  - `csv`
  - `os`
  - `sys`

## Descripción

El proyecto permite la carga y visualización de datos desde un archivo CSV, simulando un sistema de base de datos en disco. La interfaz gráfica permite visualizar los registros cargados y realizar manipulaciones sobre los mismos.

### Funcionalidades

- **Cargar Registros**: Carga los registros desde un archivo CSV y los inserta en una estructura de disco simulado.
- **Configuración**: Permite configurar los parámetros del disco, como el número de platos, pistas, sectores, y tamaño de los sectores.
- **Interfaz Visual**: Utiliza PyQt6 para mostrar los datos en una interfaz gráfica interactiva.

## Cómo Ejecutar

1. Clona o descarga el repositorio.
2. Asegúrate de tener Python 3.x y PyQt6 instalados.
3. Ejecuta el archivo `main.py` para iniciar la aplicación.

```bash
python main.py
```

### Archivos Principales

- `main.py`: Archivo principal donde se configura y ejecuta la aplicación.
- `producto.csv`: Archivo CSV que contiene los datos a cargar.
- `disco/`: Contiene la lógica de gestión del disco simulado.
- `interfaz/`: Contiene la lógica de la interfaz gráfica.
- `util/`: Contiene funciones auxiliares como el procesamiento de registros.

## Contribuciones

Si deseas contribuir a este proyecto, por favor abre un "pull request" con tus cambios.
