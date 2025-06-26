
from disco.disco import DISCOLBA
from memoria.arbol_avl import AVLIndex
from util.estructura import empaquetar, desempaquetar

class BaseDeDatosFiltrado:
    def __init__(self, disco=None):
        self.disco = disco if disco is not None else DISCOLBA()
        self.tablas = {}

    def definir_tabla(self, nombre_tabla, estructura):
        columnas = [col for col, _ in estructura]
        tipos = {
            col: (int if tipo == 'i' else
                    float if tipo == 'd' else
                    bool if tipo == '?' else
                    str)
            for col, tipo in estructura
        }

        self.tablas[nombre_tabla] = {
            'estructura': estructura,
            'columnas': columnas,
            'tipos': tipos,
            'indices': {col: AVLIndex() for col in columnas},
            'registros': {}
        }

    def cargar_datos(self, nombre_tabla, filas):
        tabla = self.tablas[nombre_tabla]
        estructura = tabla['estructura']

        for fila in filas:
            id_reg = f"{nombre_tabla}_{len(tabla['registros']) + 1}"
            binario = empaquetar(estructura, fila)
            self.disco.guardar_dato(binario, id_reg)
            ubicacion = self.disco.obtener_ubicacion(id_reg)

            for (col, _), val in zip(estructura, fila):
                if tabla['indices'][col] is None:
                    tabla['indices'][col] = AVLIndex()
                tabla['indices'][col].insertar(val, id_reg, ubicacion)

            tabla['registros'][id_reg] = ubicacion

    def buscar_por_campo(self, nombre_tabla, columna, valor):
        tabla = self.tablas[nombre_tabla]
        estructura = tabla['estructura']

        if not valor.strip():
            resultados = []
            for id_reg, ubicacion in tabla['registros'].items():
                data = self.disco.recuperar_dato(id_reg)
                if data:
                    fila = desempaquetar(estructura, data)
                    resultado = {
                        "id": id_reg,
                        "registro": {col: val for (col, _), val in zip(estructura, fila)},
                        "ubicacion": self.disco.obtener_ubicacion(id_reg)
                    }
                    resultados.append(resultado)
            return resultados

        if not columna or not columna.strip():
            return []

        tipo = tabla['tipos'].get(columna, str)
        try:
            valor_convertido = tipo(valor)
        except:
            return []

        if tabla['indices'][columna] is None:
            avl = AVLIndex()
            for id_reg, ubicacion in tabla['registros'].items():
                data = self.disco.recuperar_dato(id_reg)
                if data:
                    fila = desempaquetar(estructura, data)
                    for (col, _), val in zip(estructura, fila):
                        if col == columna:
                            avl.insertar(val, id_reg, ubicacion)
                            break
            tabla['indices'][columna] = avl

        avl = tabla['indices'][columna]
        coincidencias = avl.buscar(valor_convertido)
        resultados = []
        for id_reg, _ in coincidencias:
            data = self.disco.recuperar_dato(id_reg)
            if data:
                fila = desempaquetar(estructura, data)
                resultado = {
                    "id": id_reg,
                    "registro": {col: val for (col, _), val in zip(estructura, fila)},
                    "ubicacion": self.disco.obtener_ubicacion(id_reg)
                }
                resultados.append(resultado)
        return resultados
