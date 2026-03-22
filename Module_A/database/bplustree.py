import math
import graphviz # Ensure you run: pip install graphviz

class BPlusTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.values = []     
        self.children = []   
        self.next = None     

class BPlusTree:
    def __init__(self, order=4):
        self.root = BPlusTreeNode(leaf=True)
        self.order = order

    # ==========================================
    # SEARCH & RANGE QUERIES
    # ==========================================
    def search(self, key):
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]

        for i, k in enumerate(node.keys):
            if k == key:
                return node.values[i]
        return None

    def range_query(self, start_key, end_key):
        results = []
        node = self.root
        
        while not node.leaf:
            i = 0
            while i < len(node.keys) and start_key >= node.keys[i]:
                i += 1
            node = node.children[i]
            
        while node is not None:
            for i, k in enumerate(node.keys):
                if start_key <= k <= end_key:
                    results.append((k, node.values[i]))
                elif k > end_key:
                    return results
            node = node.next
            
        return results

    def get_all(self):
        results = []
        node = self.root
        while not node.leaf:
            node = node.children[0]
        while node is not None:
            for i in range(len(node.keys)):
                results.append((node.keys[i], node.values[i]))
            node = node.next
        return results

    # ==========================================
    # INSERTION & SPLITTING
    # ==========================================
    def insert(self, key, value):
        root = self.root
        if len(root.keys) == self.order - 1:
            new_root = BPlusTreeNode(leaf=False)
            self.root = new_root
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, key, value)
        else:
            self._insert_non_full(root, key, value)

    def _insert_non_full(self, node, key, value):
        if node.leaf:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if i < len(node.keys) and node.keys[i] == key:
                node.values[i] = value 
            else:
                node.keys.insert(i, key)
                node.values.insert(i, value)
        else:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            if len(node.children[i].keys) == self.order - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def _split_child(self, parent, index):
        child = parent.children[index]
        new_node = BPlusTreeNode(leaf=child.leaf)
        
        mid = len(child.keys) // 2 

        if child.leaf:
            new_node.keys = child.keys[mid:]
            new_node.values = child.values[mid:]
            child.keys = child.keys[:mid]
            child.values = child.values[:mid]
            
            parent.keys.insert(index, new_node.keys[0])
            parent.children.insert(index + 1, new_node)
            
            new_node.next = child.next
            child.next = new_node
        else:
            promoted_key = child.keys[mid]
            new_node.keys = child.keys[mid + 1:]
            new_node.children = child.children[mid + 1:]
            
            child.keys = child.keys[:mid]
            child.children = child.children[:mid + 1]
            
            parent.keys.insert(index, promoted_key)
            parent.children.insert(index + 1, new_node)

    # ==========================================
    # LAZY DELETION (Benchmark Safe)
    # ==========================================
    def delete(self, key):
        """
        Hyper-fast Lazy Deletion: Routes directly to the leaf and removes the data.
        Leaves internal routing keys intact to prevent cascading underflow crashes.
        """
        if not self.root:
            return False
            
        # 1. Traverse down to the correct leaf
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]

        # 2. We are at the leaf. Remove the key and value if it exists.
        for i, k in enumerate(node.keys):
            if k == key:
                node.keys.pop(i)
                node.values.pop(i)
                return True
                
        return False

    def update(self, key, new_value):
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
        
        for i, k in enumerate(node.keys):
            if k == key:
                node.values[i] = new_value
                return True
        return False

    # ==========================================
    # VISUALIZATION (Graphviz)
    # ==========================================
    def visualize_tree(self):
        dot = graphviz.Digraph(comment='B+ Tree')
        dot.attr(node={'shape': 'record'})
        
        if self.root:
            self._add_nodes(dot, self.root)
            self._add_edges(dot, self.root)
            
            node = self.root
            while not node.leaf:
                if node.children:
                    node = node.children[0]
                else:
                    break
            
            while node and node.next:
                dot.edge(str(id(node)), str(id(node.next)), style='dashed', constraint='false')
                node = node.next
                
        return dot

    def _add_nodes(self, dot, node):
        if node.leaf:
            label = " | ".join([f"<{i}> {key}:{val}" for i, (key, val) in enumerate(zip(node.keys, node.values))])
        else:
            label = " | ".join([f"<{i}> {key}" for i, key in enumerate(node.keys)])
            
        dot.node(str(id(node)), label)
        
        if not node.leaf:
            for child in node.children:
                self._add_nodes(dot, child)

    def _add_edges(self, dot, node):
        if not node.leaf:
            for i, child in enumerate(node.children):
                dot.edge(f"{id(node)}", str(id(child)))
                self._add_edges(dot, child)