from .nodo_avl import TreeNode

def getHeight(nodo):
    if nodo == None :
        return 0
    return nodo.altura

def maximo(a, b):
    return a if a > b else b

def RT_izq(A):
    x = A.right
    t2 = x.left
    
    x.left = A
    A.right = t2
    
    A.altura = maximo(getHeight(A.right), getHeight(A.left)) + 1
    x.altura = maximo(getHeight(x.right), getHeight(x.left)) + 1
    
    A.estatus = getHeight(A.right) - getHeight(A.left)
    x.estatus = getHeight(x.right) - getHeight(x.left)
    
    return x

def RT_drc(A):
    y = A.left
    t2 = y.right
    
    y.right = A
    A.left = t2
    
    A.altura = maximo(getHeight(A.right), getHeight(A.left)) + 1
    y.altura = maximo(getHeight(y.right), getHeight(y.left)) + 1
    
    A.estatus = getHeight(A.right) - getHeight(A.left)
    y.estatus = getHeight(y.right) - getHeight(y.left)
    
    return y


class BinaryTree:
    def __init__(self):
        self.root = None
        self.toggle = False
        self.recorrido = []

    def _find(self, v):
        parent = None
        current = self.root
        while current and current.value != v:
            next_node = current.left if v < current.value else current.right
            if current:
                self.recorrido.append((current, v < current.value))
            parent = current
            current = next_node
        return parent, current

    def insert(self, v):
        if self.root is None:
            self.root = TreeNode(v)
            return True
        
        self.recorrido.clear()
        parent, node = self._find(v)
        if node:
            return False

        new_node = TreeNode(v)
        
        if v < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self.recorrido.append((parent, v < parent.value))
        
        for i in range( len(self.recorrido)-1, -1, -1):
            n, _ = self.recorrido[i]
            
            n.altura = maximo( getHeight( n.left ), getHeight( n.right ) ) + 1
            
            n.estatus = getHeight(n.right) - getHeight(n.left)
            
            if n.estatus > 1 and v > n.right.value:
                nuevo = RT_izq(n)
            elif n.estatus < -1 and v > n.left.value:
                nuevo = RT_drc(n)
            elif n.estatus > 1 and v < n.right.value:
                n.right = RT_drc(n.right)
                nuevo = RT_izq(n)
            elif n.estatus < -1 and v < n.left.value:
                n.left = RT_izq(n.left)
                nuevo = RT_drc(n)
            else:
                # rotacion no necesaria
                continue
            
            if i == 0:
                self.root = nuevo
            else:
                padre, es_izquierdo = self.recorrido[i-1]
                if es_izquierdo:
                    padre.left = nuevo
                else:
                    padre.right = nuevo
                    
        return True
    
    def find(self, value):
        _, node = self._find(value)
        return node is not None

def imprimir_arbol (head, nivel = 0):
    if head is None:
        return
    imprimir_arbol (head.right, nivel + 1)
    for _ in range(nivel):
        print("    ", end="")
    print(head.value)
    imprimir_arbol(head.left, nivel + 1)

