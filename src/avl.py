# src/avl.py
# Arquivo base da AVL. 
# A implementação específica para a Etapa 5 (AVL por Pontos) 
# será feita em src/avl_points.py para cumprir o requisito de nome.

# src/avl_points.py
from .data_structs import Team
from typing import Any, List, Tuple

class AVLNode:
    """
    Classe que representa um nó em uma árvore AVL (balanceada).
    Key: Score (pontos) do time.
    Value: Objeto Team.
    """
    def __init__(self, key: int, value: Team):
        self.key = key 
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLPointsTree_A:
    """
    Implementação de uma Árvore AVL para organizar times por pontuação (score).
    """
    def __init__(self):
        self.root = None

    def _get_height(self, node: AVLNode) -> int:
        """Retorna a altura de um nó (0 se nulo)."""
        if not node:
            return 0
        return node.height

    def _get_balance(self, node: AVLNode) -> int:
        """Calcula o fator de balanceamento (Altura Esquerda - Altura Direita)."""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _left_rotate(self, z: AVLNode) -> AVLNode:
        """Realiza uma Rotação Simples à Esquerda (Case: Direita-Direita)."""
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _right_rotate(self, z: AVLNode) -> AVLNode:
        """Realiza uma Rotação Simples à Direita (Case: Esquerda-Esquerda)."""
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def insert(self, team: Team):
        """Insere um novo nó na AVL, realizando rotações se necessário."""
        self.root = self._insert(self.root, team.score, team)

    def _insert(self, node: AVLNode, key: int, value: Team) -> AVLNode:
        """Método recursivo para inserção e rebalanceamento."""
        
        # 1. Inserção de BST
        if not node:
            return AVLNode(key, value)
        
        # Se as chaves são iguais (mesmo score), vamos para a direita.
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        else:
            node.right = self._insert(node.right, key, value)

        # 2. Atualiza a altura
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        
        # 3. Obtém o fator de balanceamento
        balance = self._get_balance(node)

        # 4. Rebalanceamento (Rotações)

        # Case LL (Esquerda-Esquerda)
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)

        # Case RR (Direita-Direita)
        if balance < -1 and key >= node.right.key:
            return self._left_rotate(node)

        # Case LR (Esquerda-Direita)
        if balance > 1 and key >= node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Case RL (Direita-Esquerda)
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def height(self) -> int:
        """Retorna a altura da árvore."""
        return self._get_height(self.root)
    
    def root(self) -> AVLNode:
        """Retorna a raiz da árvore."""
        return self.root

    def inorder(self) -> List[Tuple[int, Team]]:
        """Retorna uma lista dos times ordenados pela pontuação (in-order)."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: AVLNode, result: List[Tuple[int, Team]]):
        """Método auxiliar recursivo para percorrer a árvore em ordem."""
        if node:
            self._inorder(node.left, result)
            result.append((node.key, node.value)) 
            self._inorder(node.right, result)