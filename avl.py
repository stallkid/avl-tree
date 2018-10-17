 
class AVLNode(object):
    """Define o nó na arvore AVL."""
 
    def __init__(self, parent, k):
        """Cria um nó.
 
        Args:
            parent: Nó pai.
            k: chave do nó.
        """
        self.key = k
        self.parent = parent
        self.left = None
        self.right = None
 
    def _str(self):
        """Métodos internos ASCII."""
        label = str(self.key)
        if self.left is None:
            left_lines, left_pos, left_width = [], 0, 0
        else:
            left_lines, left_pos, left_width = self.left._str()
        if self.right is None:
            right_lines, right_pos, right_width = [], 0, 0
        else:
            right_lines, right_pos, right_width = self.right._str()
        middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
        pos = left_pos + middle // 2
        width = left_pos + middle + right_width - right_pos
        while len(left_lines) < len(right_lines):
            left_lines.append(' ' * left_width)
        while len(right_lines) < len(left_lines):
            right_lines.append(' ' * right_width)
        if (middle - len(label)) % 2 == 1 and self.parent is not None and \
           self is self.parent.left and len(label) < middle:
            label += '.'
        label = label.center(middle, '.')
        if label[0] == '.': label = ' ' + label[1:]
        if label[-1] == '.': label = label[:-1] + ' '
        lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                 ' ' * left_pos + '/' + ' ' * (middle-2) +
                 '\\' + ' ' * (right_width - right_pos)] + \
          [left_line + ' ' * (width - left_width - right_width) + right_line
           for left_line, right_line in zip(left_lines, right_lines)]
        return lines, pos, width
 
    def __str__(self):
        return '\n'.join(self._str()[0])
 
    def find(self, k):
        """Encontra e retorna o nó com a chave k  dos sub nós deste nó pai.
 
        Args:
            k: a chave do nó que queremos encontrar.
 
        Retorna:
            Nó com a chave k.
        """
        if k == self.key:
            return self
        elif k < self.key:
            if self.left is None:
                return None
            else:
                return self.left.find(k)
        else:
            if self.right is None:  
                return None
            else:
                return self.right.find(k)
 
    def find_min(self):
        """ Encontra o nó de chave minima com os sub nós do nó pai.
 
        Retorna:
            Nó com a menor chave.
        """
        current = self
        while current.left is not None:
            current = current.left
        return current
 
    def next_larger(self):
        """Retorna o nó com a proxima maior chave (sucessor) na árvore.
        """
        if self.right is not None:
            return self.right.find_min()
        current = self
        while current.parent is not None and current is current.parent.right:
            current = current.parent
        return current.parent
 
    def insert(self, node):
        """ Insere no sub nó do nó pai.
 
        Args:
            node: Nó inserido.
        """
        if node is None:
            return
        if node.key < self.key:
            if self.left is None:
                node.parent = self
                self.left = node
            else:
                self.left.insert(node)
        else:
            if self.right is None:
                node.parent = self
                self.right = node
            else:
                self.right.insert(node)
 
    def delete(self):
        """Deleta e retorna o nó da árvore."""
        if self.left is None or self.right is None:
            if self is self.parent.left:
                self.parent.left = self.left or self.right
                if self.parent.left is not None:
                    self.parent.left.parent = self.parent
            else:
                self.parent.right = self.left or self.right
                if self.parent.right is not None:
                    self.parent.right.parent = self.parent
            return self
        else:
            s = self.next_larger()
            self.key, s.key = s.key, self.key
            return s.delete()
 
def height(node):
    if node is None:
        return -1
    else:
        return node.height
 
def update_height(node):
    node.height = max(height(node.left), height(node.right)) + 1
 
class AVL(object):
    """
    Implementação AVL da busca na árvore binária.
    """
 
    def __init__(self):
        """ Árvore vazia """
        self.root = None
 
    def __str__(self):
        if self.root is None: return '<Árvore vazia>'
        return str(self.root)
 
    def find(self, k):
        """ Encontra e retorna o nó com chave k dos sub nó atrelados no nó pai.
 
        Args:
            k: A chave do nó que desejamos encontrar.
 
        Retorna:
            O nó com chave k ou nada se a árvore estiver.
        """
        return self.root and self.root.find(k)
 
    def find_min(self):
        """Retorna o menor nó da busca."""
 
        return self.root and self.root.find_min()
 
    def next_larger(self, k):
        """ Retorna o nó que contem o proxima maior chave (Sucessor) nas buscas relacionadas ao nó com chave k.
 
        Args:
            k: Chave com o nó que o sucessor deve encontrar.
 
        Retorna:
            Próximo nó.
        """
        node = self.find(k)
        return node and node.next_larger()   
 
    def left_rotate(self, x):
        y = x.right
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.right = y.left
        if x.right is not None:
            x.right.parent = x
        y.left = x
        x.parent = y
        update_height(x)
        update_height(y)
 
    def right_rotate(self, x):
        y = x.left
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.left = y.right
        if x.left is not None:
            x.left.parent = x
        y.right = x
        x.parent = y
        update_height(x)
        update_height(y)
 
    def rebalance(self, node):
        while node is not None:
            update_height(node)
            if height(node.left) >= 2 + height(node.right):
                if height(node.left.left) >= height(node.left.right):
                    self.right_rotate(node)
                else:
                    self.left_rotate(node.left)
                    self.right_rotate(node)
            elif height(node.right) >= 2 + height(node.left):
                if height(node.right.right) >= height(node.right.left):
                    self.left_rotate(node)
                else:
                    self.right_rotate(node.right)
                    self.left_rotate(node)
            node = node.parent
 
    def insert(self, k):
        """ Insere o nó com chave k no sub nó atrelado ao nó pai.
 
        Args:
            k: Chave do nó a ser inserido.
        """
        node = AVLNode(None, k)
        if self.root is None:
            # The root's parent is None.
            self.root = node
        else:
            self.root.insert(node)
        self.rebalance(node)
 
    def delete(self, k):
        """Deleta e retorna o nó com chave k se existir na busca.
 
        Args:
            k: Chave do nó que deseja excluir.
 
        Retorna:
            Nó excluido com a chave k.
        """
        node = self.find(k)
        if node is None:
            return None
        if node is self.root:
            pseudoroot = AVLNode(None, 0)
            pseudoroot.left = self.root
            self.root.parent = pseudoroot
            deleted = self.root.delete()
            self.root = pseudoroot.left
            if self.root is not None:
                self.root.parent = None
        else:
            deleted = node.delete()   
        ## node.parent é o antigo pai do nó,
        ## Provavel nó não balanceado.
        self.rebalance(deleted.parent)
 
def test(args=None):
    import random, sys
    if not args:
        args = sys.argv[1:]
    if not args:
        print('usage: %s <number-of-random-items | item item item ...>' % \
              sys.argv[0])
        sys.exit()
    elif len(args) == 1:
        items = (random.randrange(100) for i in range(int(args[0])))
    else:
        items = [int(i) for i in args]
 
    tree = AVL()
    print(tree)
    for item in items:
        tree.insert(item)
        print()
        print(tree)
 
if __name__ == '__main__': test()