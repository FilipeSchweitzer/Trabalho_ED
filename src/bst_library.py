# src/bst.py
from .data_structs import Team
from typing import List, Tuple, Any

class Node:
    """
    Classe que representa um nó em uma árvore binária de busca (BST).
    """
    def __init__(self, key: Any, value: Team):
        self.key = key      # Chave de ordenação (ex: nome ou score)
        self.value = value  # Objeto Team
        self.left = None
        self.right = None

class BST_A:
    """
    Classe que implementa uma árvore binária de busca (BST) simples.
    Usada para armazenar seleções ordenadas por chave (nome ou score).
    """
    def __init__(self):
        self.root = None

    def insert(self, key: Any, value: Team):
        """Insere um novo nó na BST com a chave e valor fornecidos."""
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert(self.root, key, value)

    def _insert(self, node: Node, key: Any, value: Team):
        """Método auxiliar recursivo para inserir um nó na posição correta."""
        # Se as chaves são iguais, o nó vai para a direita para evitar duplicação 
        # (especialmente útil para scores iguais).
        if key < node.key:
            if node.left is None:
                node.left = Node(key, value)
            else:
                self._insert(node.left, key, value)
        else: # key >= node.key
            if node.right is None:
                node.right = Node(key, value)
            else:
                self._insert(node.right, key, value)

    def inorder(self) -> List[Tuple[Any, Team]]:
        """Retorna uma lista com os nós em ordem crescente (in-order traversal)."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Node, result: List[Tuple[Any, Team]]):
        """Método auxiliar recursivo para percorrer a árvore em ordem."""
        if node:
            self._inorder(node.left, result)
            result.append((node.key, node.value))
            self._inorder(node.right, result)

    def search(self, key: Any) -> Team | None:
        """Busca um time pela chave na BST."""
        return self._search(self.root, key)

    def _search(self, node: Node, key: Any) -> Team | None:
        if node is None or node.key == key:
            return node.value if node else None
        
        if key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)