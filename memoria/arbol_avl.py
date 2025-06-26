class NodoAVL:
    def __init__(self, clave, fragmentos):
        self.clave = clave
        self.fragmentos = [fragmentos]  # lista de fragmentos asociados
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class AVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, clave, fragmentos):
        self.raiz = self._insertar(self.raiz, clave, fragmentos)

    def _insertar(self, nodo, clave, fragmentos):
        if not nodo:
            return NodoAVL(clave, fragmentos)

        if clave == nodo.clave:
            nodo.fragmentos.append(fragmentos)
        elif clave < nodo.clave:
            nodo.izquierda = self._insertar(nodo.izquierda, clave, fragmentos)
        else:
            nodo.derecha = self._insertar(nodo.derecha, clave, fragmentos)

        nodo.altura = 1 + max(self._altura(nodo.izquierda),
                                self._altura(nodo.derecha))

        balance = self._balance(nodo)

        if balance > 1 and clave < nodo.izquierda.clave:
            return self._rotar_derecha(nodo)
        if balance < -1 and clave > nodo.derecha.clave:
            return self._rotar_izquierda(nodo)
        if balance > 1 and clave > nodo.izquierda.clave:
            nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
            return self._rotar_derecha(nodo)
        if balance < -1 and clave < nodo.derecha.clave:
            nodo.derecha = self._rotar_derecha(nodo.derecha)
            return self._rotar_izquierda(nodo)

        return nodo

    def buscar(self, clave):
        return self._buscar(self.raiz, clave)

    def _buscar(self, nodo, clave):
        if not nodo:
            return []
        if clave == nodo.clave:
            return nodo.fragmentos
        elif clave < nodo.clave:
            return self._buscar(nodo.izquierda, clave)
        else:
            return self._buscar(nodo.derecha, clave)

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _balance(self, nodo):
        return self._altura(nodo.izquierda) - self._altura(nodo.derecha) if nodo else 0

    def _rotar_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha

        y.derecha = z
        z.izquierda = T3

        z.altura = 1 + max(self._altura(z.izquierda), self._altura(z.derecha))
        y.altura = 1 + max(self._altura(y.izquierda), self._altura(y.derecha))

        return y

    def _rotar_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda

        y.izquierda = z
        z.derecha = T2

        z.altura = 1 + max(self._altura(z.izquierda), self._altura(z.derecha))
        y.altura = 1 + max(self._altura(y.izquierda), self._altura(y.derecha))

        return y

    def in_order(self):
        return self._in_order(self.raiz)

    def _in_order(self, nodo):
        if not nodo:
            return []
        return (self._in_order(nodo.izquierda) +
                [(nodo.clave, nodo.fragmentos)] +
                self._in_order(nodo.derecha))
