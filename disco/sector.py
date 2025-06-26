class Sector:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.campos = []

    def espacio_libre(self):
        return self.capacidad - self.uso_memoria()

    def uso_memoria(self, string = 40):
        total = 0
        for campo in self.campos:
            if campo["tipo"] == "int":
                total += 4
            elif campo["tipo"] == "char":
                total += 1
            elif campo["tipo"] == "float":
                total += 4
            elif campo["tipo"] == "double":
                total += 8
            elif campo["tipo"] == "bool":
                total += 1
            elif campo["tipo"] == "string":
                total += len(campo["valor"]) + 1
                
        return total

    def agregar_campo(self, tipo, valor):
        peso = self._peso_tipo(tipo, valor)
        if self.espacio_libre() >= peso:
            inicio = self.uso_memoria()
            fin = inicio + peso - 1
            self.campos.append({
                "tipo": tipo,
                "valor": valor,
                "inicio": inicio,
                "fin": fin
            })
            return inicio, fin
        return None

    def _peso_tipo(self, tipo, valor):
        if tipo == "int":
            return 4
        elif tipo == "char":
            return 1
        elif tipo == "float":
            return 4
        elif tipo == "double":
            return 8
        elif tipo == "bool":
            return 1
        elif tipo == "string":
            return len(valor) + 1
        else:
            raise ValueError(f"Tipo no soportado: {tipo}")

    def __str__(self):
        contenido = " | ".join(
            f"{c['valor']} ({c['tipo']}) [{c['inicio']}-{c['fin']}]" for c in self.campos
        )
        return f"| {contenido} | espacio libre ({self.espacio_libre()} bytes) |"

